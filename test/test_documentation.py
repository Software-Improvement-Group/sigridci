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

import os
import re
import unittest


class DocumentationTest(unittest.TestCase):
    LINK = re.compile("\\[(.*?)\\]\\((\\S+)\\)")
    IMAGE = re.compile("img src=\"(\\S+)\"")

    def testDocumentationDoesNotContainDeadLinks(self):
        for file, contents in self.readDocumentationPages():
            for match in self.LINK.finditer(contents):
                if match.group(2).endswith(".md"):
                    parentDir = os.path.dirname(file)
                    linkedFile = os.path.join(parentDir, match.group(2))
                    self.assertTrue(os.path.exists(linkedFile), f"Dead link in {file} to {linkedFile}")
                    
    def testDocumentationDoesNotContainDeadImages(self):
        for file, contents in self.readDocumentationPages():
            for match in self.IMAGE.finditer(contents):
                parentDir = os.path.dirname(file)
                linkedFile = os.path.join(parentDir, match.group(1))
                self.assertTrue(os.path.exists(linkedFile), f"Dead image in {file} to {linkedFile}")
        
    def readDocumentationPages(self):
        for root, subdirs, files in os.walk("docs"):
            for file in files:
                if file.endswith(".md"):
                    with open(f"{root}/{file}", "r") as fileRef:
                        yield (f"{root}/{file}", fileRef.read())
