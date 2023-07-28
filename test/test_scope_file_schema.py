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

import json
import jsonschema
import unittest
import yaml


class ScopeFileSchemaTest(unittest.TestCase):
    maxDiff = None
    
    def setUp(self):
        with open("resources/sigrid-scope-file.schema.json", "r") as f:
            self.schema = json.load(f)

    def testSchemaIsValidJson(self):
        self.assertEqual(list(self.schema.keys()),
            ["$schema", "title", "description", "definitions", "type", "required", "properties", "additionalProperties"])
            
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
