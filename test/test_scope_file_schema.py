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
