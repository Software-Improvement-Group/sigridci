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
import yaml
from bs4 import BeautifulSoup
from unittest import TestCase


class DocumentationTest(TestCase):
    LINK = re.compile("\\[(.*?)\\]\\((\\S+)\\)")
    IMAGE = re.compile("img src=\"(\\S+)\"")

    def testDocumentationDoesNotContainBrokenLinks(self):
        for file, contents in self.readDocumentationPages():
            for match in self.LINK.finditer(contents):
                if ".md" in match.group(2) and not match.group(2).startswith("https://"):
                    parentDir = os.path.dirname(file)
                    linkedFile = os.path.join(parentDir, match.group(2).split(".md")[0] + ".md")
                    self.assertTrue(os.path.exists(linkedFile), f"Dead link in {file} to {linkedFile}")
                elif "docs.sigrid-says.com" in match.group(2) and not file.endswith("README.md"):
                    self.fail(f"{file} should link to relative .md file, not to the absolute URL: {match.group(2)}")
                                        
    def testDocumentationDoesNotContainDeadImages(self):
        for file, contents in self.readDocumentationPages():
            for match in self.IMAGE.finditer(contents):
                parentDir = os.path.dirname(file)
                linkedFile = os.path.join(parentDir, match.group(1))
                self.assertTrue(os.path.exists(linkedFile), f"Dead image in {file} to {linkedFile}")
                
    def testMenuDoesNotContainDeadLinks(self):
        with open("docs/_includes/menu.html", "r") as f:
            dom = BeautifulSoup(f.read(), features="html.parser")
        
        for menuLink in dom.select("a.page"):
            if not menuLink["href"].startswith("https://"):
                linkedFile = f"docs{menuLink['href']}".split("#")[0].replace(".html", ".md")
                self.assertTrue(os.path.exists(linkedFile), f"Dead menu link to {linkedFile}")
                
    def testFileNamesAreLowercase(self):
        for file, contents in self.readDocumentationPages():
            if not file.lower().endswith("readme.md"):
                self.assertEqual(file, file.lower(), f"Article file name should be lowercase: {file}")
            
        for file in self.listDocumentationImages():
            self.assertEqual(file, file.lower(), f"Image file name should be lowercase: {file}")
            
    def testMarkdownShouldNotContainSmartQuotes(self):
        for file, contents in self.readDocumentationPages():
            for line in contents.split("\n"):
                if "\u201B" in line or "\u201C" in line or "\u201D" in line or "\u201F" in line:
                    self.fail(f"{file} contains smart quote characters, which is likely unintentional:\n{line}")

    def testPagesShouldNotDefineTheirOwnTableOfContents(self):
        for file, contents in self.readDocumentationPages():
            for line in contents.split("\n"):
                if "<sig-toc>" in line:
                    self.fail(f"{file} should not define it's own table of contents")

    def testTechnologySupportListShouldMatchYaml(self):
        with open("resources/technologies.yaml", "r") as f:
            technologyList = yaml.safe_load(f)
            technologyMap = {tech["context"]: tech for tech in technologyList}

        with open("docs/reference/technology-support.md", "r") as f:
            rows = [line for line in f.readlines() if line.startswith("| `")]
            getCells = lambda row: [cell.replace("`", "").strip() for cell in row.split("|") if cell != ""]
            supportTable = [getCells(row) for row in rows]

        for row in supportTable:
            if row[0] not in technologyMap:
                self.fail(f"Technology '{row[0]}' is not defined in technologies.yaml")

        for tech in technologyList:
            if tech["context"] not in [row[0] for row in supportTable] and tech["context"] != "unknown":
                self.fail(f"Technology '{tech['context']}' is not defined in technology support table")

    def readDocumentationPages(self):
        with open("README.md", "r") as fileRef:
            yield ("README.md", fileRef.read())
    
        for root, subdirs, files in os.walk("docs"):
            for file in files:
                if file.endswith(".md"):
                    with open(f"{root}/{file}", "r") as fileRef:
                        yield (f"{root}/{file}", fileRef.read())

    def listDocumentationImages(self):
        for root, subdirs, files in os.walk("docs"):
            for file in files:
                if file.lower().endswith((".png", ".jpg")):
                    yield f"{root}/{file}"
