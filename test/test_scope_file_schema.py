# Copyright Software Improvement Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect
import json
import jsonschema
import yaml
from textwrap import dedent
from unittest import TestCase


class ScopeFileSchemaTest(TestCase):
    maxDiff = None
    
    def setUp(self):
        with open("resources/sigrid-scope-file.schema.json", "r") as f:
            self.schema = json.load(f)

    def testSchemaIsValidJson(self):
        fields = [
            "$id",
            "$schema",
            "additionalProperties",
            "definitions",
            "description", 
            "properties",
            "required",
            "title",
            "type"
        ]
    
        self.assertEqual(sorted(self.schema.keys()), fields)
            
    def testValidScopeFileAgainstSchema(self):
        scope = """
            languages:
              - Java
              - Python
            """
            
        parsedScope = yaml.load(scope, Loader=yaml.FullLoader)
        jsonschema.validate(instance=parsedScope, schema=self.schema)
    
    def testInvalidScopeFileAgainstSchema(self):
        scope = """
            languages:
              - Java
              - name: Python
                includes:
                  - ".*[.]x"
            """
        
        try:
            parsedScope = yaml.load(scope, Loader=yaml.FullLoader)
            jsonschema.validate(instance=parsedScope, schema=self.schema)
        except jsonschema.ValidationError as e:
            self.assertEqual("$.languages[1]", e.json_path)

    def testDisallowedSection(self):
        scope = """
                languages:
                  - Java
                checkmarx:
                  aap: true
                """

        try:
            parsedScope = yaml.load(scope, Loader=yaml.FullLoader)
            jsonschema.validate(instance=parsedScope, schema=self.schema)
            self.assertTrue(False, "ValidationError should have been raised")
        except jsonschema.ValidationError as e:
            self.assertTrue("schema does not allow {'aap': True}" in e.message)

    def testDependencyCheckerExcludeOptions(self):
        scope = """
            languages:
              - Python
            dependencychecker:
              exclude:
                - "aap"
                - path: "noot"
                - vulnerability: "CVE-123"
                - license: "mies"
                - activity: "boom"
                - management: "jan"
                - freshness: "henk:.*"
            """
            
        parsedScope = yaml.load(scope, Loader=yaml.FullLoader)
        jsonschema.validate(instance=parsedScope, schema=self.schema)
        
    def testRejectUnknownDependencyCheckerExcludeOptions(self):
        scope = """
            languages:
              - Python
            dependencychecker:
              exclude:
                - something: "noot"
            """
            
        try:
            parsedScope = yaml.load(scope, Loader=yaml.FullLoader)
            jsonschema.validate(instance=parsedScope, schema=self.schema)
            self.assertTrue(False, "ValidationError should have been raised")
        except jsonschema.ValidationError as e:
            self.assertTrue("{'something': 'noot'} is not valid under any of the given schemas" in e.message)

    def testDependencyCheckerSourceOption(self):
        base = inspect.cleandoc("""
            languages:
              - Python
            dependencychecker:
              blocklist: ["NONE"]
            """)

        scope = yaml.load(f"{base}\n  source: all", Loader=yaml.FullLoader)
        jsonschema.validate(instance=scope, schema=self.schema)

        scope = yaml.load(f"{base}\n  source: sbom", Loader=yaml.FullLoader)
        jsonschema.validate(instance=scope, schema=self.schema)

        try:
            scope = yaml.load(f"{base}\n  source: aap", Loader=yaml.FullLoader)
            jsonschema.validate(instance=scope, schema=self.schema)
            self.assertTrue(False, "ValidationError should have been raised")
        except jsonschema.ValidationError as e:
            self.assertTrue("'aap' is not one of ['all', 'sbom']" in e.message)

    def testArchitectureRoleOption(self):
        scope = """
            languages:
              - Python
            architecture:
              component_roles:
                - role: utility
                  include:
                    - ".*util.*"
            """

        parsedScope = yaml.load(scope, Loader=yaml.FullLoader)
        jsonschema.validate(instance=parsedScope, schema=self.schema)

    def testDanglingExcludeOptionIsError(self):
        scope = """
            languages:
              - Python
            exclude:
            """

        try:
            parsedScope = yaml.load(scope, Loader=yaml.FullLoader)
            jsonschema.validate(instance=parsedScope, schema=self.schema)
            self.assertTrue(False, "ValidationError should have been raised")
        except jsonschema.ValidationError as e:
            self.assertTrue("None is not of type 'array'" in e.message)

    def testBlocklistIsNotRequired(self):
        scope = """
            languages:
              - Python
            dependencychecker:
              exclude:
                - ".*aap.*"
            """

        parsedScope = yaml.load(scope, Loader=yaml.FullLoader)
        jsonschema.validate(instance=parsedScope, schema=self.schema)

    def testTpfEnabledPropertyIsNotRequired(self):
        scope = """
            languages:
              - Python
            thirdpartyfindings:
              exclude:
                - ".*/scripts/.*[.]sh"
            """

        parsedScope = yaml.load(scope, Loader=yaml.FullLoader)
        jsonschema.validate(instance=parsedScope, schema=self.schema)

    def testAllPossibleScopeFileFieldsAreKnown(self):
        def getProperties(element):
            properties = element.get("properties", {}) | element.get("items", {}).get("properties", {})
            for alternative in element.get("anyOf", []):
                properties = properties | alternative.get("properties", {})
            return [(name, properties[name]) for name in sorted(properties.keys())]

        def format(name, element, indent):
            result = f"{'  ' * indent}{name}\n"
            for propertyName, property in getProperties(element):
                if isinstance(property, dict):
                    result += format(propertyName, property, indent + 1)
                    if property.get("$ref"):
                        definitionName = property["$ref"].split("/")[-1]
                        definition = self.schema["definitions"][definitionName]
                        for defPropertyName, defProperty in getProperties(definition):
                            result += format(defPropertyName, defProperty, indent + 2)
            return result

        expected = dedent("""
            schema
              architecture
                add_dependencies
                add_system_elements
                branch
                co_evolution
                component_roles
                custom_components
                custom_patterns
                disabled_metrics
                duplication
                enabled
                exclude
                file_annotation_components
                flatten_directories
                grouping
                history
                history_enabled
                history_end
                history_filter_outliers
                history_interval
                history_period_months
                history_start
                merge_data_stores
                model
                remove_dependencies
                remove_system_elements
                rename
                undesirable_dependencies
              component_base_dirs
              component_depth
              components
                exclude
                include
                name
              default_excludes
              dependencychecker
                blacklist
                blocklist
                enabled
                exclude
                model
                override_disabled_technologies
                override_enabled_technologies
                source
                transitive
              exclude
              experimental
              languages
              model
              thirdpartyfindings
                disabled_analyzers
                disabled_rules
                enabled
                enabled_analyzers
                enabled_rules
                exclude
                include
        """)

        self.assertEqual(expected.strip(), format("schema", self.schema, 0).strip())
