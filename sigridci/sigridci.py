#!/usr/bin/env python3

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

import argparse
import base64
import datetime
import html
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import zipfile


def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}  {message}")


class SigridApiClient:
    PROTOCOL_VERSION = "v1"
    POLL_INTERVAL = 60
    POLL_ATTEMPTS = 30

    def __init__(self, args):
        self.baseURL = args.sigridurl
        self.account = os.environ["SIGRID_CI_ACCOUNT"]
        self.token = os.environ["SIGRID_CI_TOKEN"]
        
        self.urlPartnerName = urllib.parse.quote_plus(args.partner.lower())
        self.urlCustomerName = urllib.parse.quote_plus(args.customer.lower())
        self.urlSystemName = urllib.parse.quote_plus(args.system.lower())
        
    def callSigridAPI(self, api, path):
        url = f"{self.baseURL}/rest/{api}{path}"
        request = urllib.request.Request(url, None)
        request.add_header("Accept", "application/json")
        request.add_header("Authorization", \
            b"Basic " + base64.urlsafe_b64encode(f"{self.account}:{self.token}".encode("utf8")))
            
        response = urllib.request.urlopen(request)
        if response.status == 204:
            return {}
        responseBody = response.read().decode("utf8")
        if len(responseBody) == 0:
            log("Received empty response")
            return {}
        return json.loads(responseBody)
        
    def submitUpload(self, sourceDir, excludePatterns, useRepoHistory):
        log("Creating upload")
        uploadPacker = SystemUploadPacker(excludePatterns, useRepoHistory)
        upload = "sigrid-upload-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".zip"
        uploadPacker.prepareUpload(sourceDir, upload)
    
        log("Preparing upload")
        requestUploadResponse = self.callSigridAPI("inboundresults",
            f"/{self.urlPartnerName}/{self.urlCustomerName}/{self.urlSystemName}/ci/uploads/{self.PROTOCOL_VERSION}")
        uploadUrl = requestUploadResponse["uploadUrl"]
        analysisId = requestUploadResponse["ciRunId"]
        log(f"Sigrid CI analysis ID: {analysisId}")
        
        log("Submitting upload")
        if not self.uploadBinaryFile(uploadUrl, upload):
            raise Exception("Uploading file failed")
            
        return analysisId
        
    def uploadBinaryFile(self, url, upload):
        with open(upload, "rb") as uploadRef:
            uploadRequest = urllib.request.Request(url, data=uploadRef.read())
            uploadRequest.method = "PUT"
            uploadRequest.add_header("Content-Type", "application/zip")
            uploadRequest.add_header("Content-Length", "%d" % os.path.getsize(upload))
            uploadRequest.add_header("x-amz-server-side-encryption", "AES256")
            uploadResponse = urllib.request.urlopen(uploadRequest)
            return uploadResponse.status in [200, 201, 202]
        
    def fetchAnalysisResults(self, analysisId):
        for attempt in range(self.POLL_ATTEMPTS):
            try:
                response = self.callSigridAPI("analysis-results",
                    f"/sigridci/{self.urlCustomerName}/{self.urlSystemName}/{self.PROTOCOL_VERSION}/ci/results/{analysisId}")
                if response != {}:
                    return response            
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    raise Exception(f"Received HTTP status {e.code}")
            
            log("Waiting for analysis results")
            time.sleep(self.POLL_INTERVAL)
            
        log("Analysis failed: waiting for analysis results took too long")
        sys.exit(1)
        

class SystemUploadPacker:
    MAX_UPLOAD_SIZE_MB = 500

    DEFAULT_EXCLUDES = [
        "coverage/",
        "build/",
        "dist/",
        "node_modules/",
        "sigridci/",
        "sigrid-ci-output/",
        "target/",
        ".idea/",
        ".jpg",
        ".png"
    ]
    
    def __init__(self, excludePatterns=[], useRepoHistory=True):
        self.excludePatterns = []
        self.excludePatterns += self.DEFAULT_EXCLUDES
        self.excludePatterns += [excl for excl in excludePatterns if excl != ""]
        if not useRepoHistory:
            self.excludePatterns += [".git"]

    def prepareUpload(self, sourceDir, outputFile):
        zipFile = zipfile.ZipFile(outputFile, "w", zipfile.ZIP_DEFLATED)
        
        for root, dirs, files in os.walk(sourceDir):
            for file in files:
                filePath = os.path.join(root, file)
                if file != outputFile and not self.isExcluded(filePath):
                    relativePath = os.path.relpath(os.path.join(root, file), sourceDir)
                    zipFile.write(filePath, relativePath)
        
        zipFile.close()
        
        uploadSizeMB = max(round(os.path.getsize(outputFile) / 1024 / 1024), 1)
        log(f"Upload size is {uploadSizeMB} MB")
        if uploadSizeMB > self.MAX_UPLOAD_SIZE_MB:
            raise Exception(f"Upload exceeds maximum size of {self.MAX_UPLOAD_SIZE_MB} MB")
        
    def isExcluded(self, filePath):
        normalizedPath = filePath.replace("\\", "/")
        for exclude in self.excludePatterns:
            if exclude.strip() in normalizedPath:
                return True
        return False
        
        
class Report:
    METRICS = ["VOLUME", "DUPLICATION", "UNIT_SIZE", "UNIT_COMPLEXITY", "UNIT_INTERFACING", "MODULE_COUPLING", \
               "COMPONENT_BALANCE_PROP", "COMPONENT_INDEPENDENCE", "COMPONENT_ENTANGLEMENT", "MAINTAINABILITY"]

    def generate(self, feedback, args):
        pass
        
    def formatRating(self, ratings, metric):
        if ratings.get(metric, None) == None:
            return "N/A"
        return "%.1f" % ratings[metric]
        
    def formatBaselineDate(self, feedback):
        snapshotDate = datetime.datetime.strptime(feedback["baseline"], "%Y%m%d")
        return snapshotDate.strftime("%Y-%m-%d")
        
    def isPassed(self, feedback, metric, targetRating):
        value = feedback["newCodeRatings"].get(metric, None)
        return value == None or value >= targetRating
        
    def getSigridUrl(self, args):
        return "https://sigrid-says.com/" + urllib.parse.quote_plus(args.customer) + "/" + \
            urllib.parse.quote_plus(args.system);


class TextReport(Report):
    ANSI_BOLD = "\033[1m"
    ANSI_GREEN = "\033[92m"
    ANSI_YELLOW = "\033[33m"
    ANSI_RED = "\033[91m"
    ANSI_BLUE = "\033[96m"
    LINE_WIDTH = 81

    def generate(self, feedback, args):
        print("-" * self.LINE_WIDTH)
        print("Refactoring candidates")
        print("-" * self.LINE_WIDTH)
        print("")
        for metric in [metric for metric in self.METRICS if metric in feedback["refactoringCandidatesPerType"]]:
            print("")
            print(metric.replace("_PROP", "").title().replace("_", " "))
            for rc in feedback["refactoringCandidatesPerType"][metric]:
                print("    - " + rc)

        print("")
        print("-" * self.LINE_WIDTH)
        print("Maintainability ratings")
        print("-" * self.LINE_WIDTH)
        print("System property".ljust(40) + f"Baseline ({self.formatBaselineDate(feedback)})    New code quality")
        for metric in self.METRICS:
            if metric == "MAINTAINABILITY":
                print("-" * self.LINE_WIDTH)
            self.printRatingColor(metric.title().replace("_", " ").ljust(40) + \
                "(" + self.formatRating(feedback["overallRatings"], metric) + ")".ljust(21) + \
                self.formatRating(feedback["newCodeRatings"], metric), feedback["newCodeRatings"].get(metric))
    
    def printRatingColor(self, message, rating):
        ansiCodes = {
            self.ANSI_GREEN : rating != None and rating >= 3.5,
            self.ANSI_YELLOW : rating != None and rating >= 2.5 and rating < 3.5,
            self.ANSI_RED : rating != None and rating >= 0.0 and rating < 2.5,
            self.ANSI_BLUE : rating == None
        }

        prefix = "".join([code for code in ansiCodes if ansiCodes[code]])
        self.printColor(message, prefix)

    def printColor(self, message, ansiPrefix):
        print(ansiPrefix + message + "\033[0m")
        
        
class StaticHtmlReport(Report):
    HTML_STAR_FULL = "&#9733;"
    HTML_STAR_EMPTY = "&#9734;"

    def generate(self, feedback, args):
        if not os.path.exists("sigrid-ci-output"):
            os.mkdir("sigrid-ci-output")
    
        with open(os.path.dirname(__file__) + "/sigridci-feedback-template.html", encoding="utf-8", mode="r") as templateRef:
            template = templateRef.read()
            template = self.renderHtmlFeedback(template, feedback, args)

        reportFile = os.path.abspath("sigrid-ci-output/index.html")
        writer = open(reportFile, encoding="utf-8", mode="w")
        writer.write(template)
        writer.close()
        
        print("")
        print("You can find the full results here:")
        print(reportFile)
        print("")
        print("You can find more information about these results in Sigrid:")
        print(self.getSigridUrl(args))
        print("")
        
    def renderHtmlFeedback(self, template, feedback, args):
        template = template.replace("@@@CUSTOMER", args.customer)
        template = template.replace("@@@SYSTEM", args.system)
        template = template.replace("@@@TARGET", "%.1f" % args.targetquality)
        template = template.replace("@@@LINES_OF_CODE_TOUCHED", "%d" % feedback.get("newCodeLinesOfCode", 0))
        template = template.replace("@@@BASELINE_DATE", self.formatBaselineDate(feedback))
        template = template.replace("@@@SIGRID_LINK", self.getSigridUrl(args))
        for metric in self.METRICS:
            template = template.replace("@@@" + metric + "_OVERALL", self.formatRating(feedback["overallRatings"], metric))
            template = template.replace("@@@" + metric + "_NEW", self.formatRating(feedback["newCodeRatings"], metric))
            template = template.replace("@@@" + metric + "_STARS_OVERALL", self.formatHtmlStars(feedback["overallRatings"], metric))
            template = template.replace("@@@" + metric + "_STARS_NEW", self.formatHtmlStars(feedback["newCodeRatings"], metric))
            passed = self.isPassed(feedback, metric, args.targetquality)
            template = template.replace("@@@" + metric + "_PASSED", "passed" if passed else "failed")
            refactoringCandidates = feedback["refactoringCandidatesPerType"].get(metric, [])
            template = template.replace("@@@" + metric + "_REFACTORING_CANDIDATES",
                "\n".join(["<span>" + html.escape(rc) + "</span>" for rc in refactoringCandidates]))
        return template
        
    def formatHtmlStars(self, ratings, metric):
        if ratings.get(metric, None) == None:
            return "N/A"
        stars = min(round(ratings[metric]), 5)
        fullStars = stars * self.HTML_STAR_FULL
        emptyStars = (5 - stars) * self.HTML_STAR_EMPTY
        rating = self.formatRating(ratings, metric)
        return f"<strong class=\"stars{stars}\">{fullStars}{emptyStars}</strong> &nbsp; " + rating
        
        
class ExitCodeReport(Report):
    def generate(self, feedback, args):
        asciiArt = TextReport()
        if self.isPassed(feedback, "MAINTAINABILITY", args.targetquality):
            asciiArt.printColor("\n** MAINTAINABILITY CHECK PASSED **\n", asciiArt.ANSI_BOLD + asciiArt.ANSI_GREEN)
        else:
            asciiArt.printColor("\n** MAINTAINABILITY CHECK FAILED **\n", asciiArt.ANSI_BOLD + asciiArt.ANSI_RED)
            sys.exit(1)
                

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--partner", type=str, default="sig")
    parser.add_argument("--customer", type=str)
    parser.add_argument("--system", type=str)
    parser.add_argument("--source", type=str)
    parser.add_argument("--targetquality", type=float, default=3.5)
    parser.add_argument("--exclude", type=str, default="")
    parser.add_argument("--history", type=str, default="none")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com")
    args = parser.parse_args()
    
    if args.customer == None or args.system == None or args.source == None:
        parser.print_help()
        sys.exit(1)
    
    if sys.version_info.major <= 2:
        print("Sigrid CI requires Python 3")
        sys.exit(1)
        
    if not "SIGRID_CI_ACCOUNT" in os.environ or not "SIGRID_CI_TOKEN" in os.environ:
        print("Sigrid account not found in environment variables SIGRID_CI_ACCOUNT and SIGRID_CI_TOKEN")
        sys.exit(1)
        
    if not os.path.exists(args.source):
        print("Source code directory not found: " + args.source)
        sys.exit(1)
    
    log("Starting Sigrid CI")
    apiClient = SigridApiClient(args)
    analysisId = apiClient.submitUpload(args.source, args.exclude.split(","), args.history != "none")
    feedback = apiClient.fetchAnalysisResults(analysisId)
    
    for report in [TextReport(), StaticHtmlReport(), ExitCodeReport()]:
        report.generate(feedback, args)
        