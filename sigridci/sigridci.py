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
import dataclasses
import html
import json
import os
import re
import sys
import time
import typing
import urllib.parse
import urllib.request
import ssl
import zipfile
import certifi

LOG_HISTORY = []
SYSTEM_NAME_PATTERN = re.compile("[a-z0-9][a-z0-9-]+", re.IGNORECASE)


def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}  {message}", flush=True)
    LOG_HISTORY.append(message)
    
    
@dataclasses.dataclass
class UploadOptions:
    sourceDir: str = None
    excludePatterns: typing.List[str] = dataclasses.field(default_factory=lambda: [])
    includeHistory: bool = False
    pathPrefix: str = ""
    showContents: bool = False
    publishOnly: bool = False
    
    
@dataclasses.dataclass
class TargetQuality:
    ratings: typing.Dict[str, float]

    def __init__(self, configFile, targetRating):
        self.ratings = {"MAINTAINABILITY" : targetRating}
        
        if os.path.exists(configFile):
            log(f"Loading target quality level from configuration file {configFile}")
            # We can't use pyyaml because PIP is not available in the some of the
            # very diverse set of customer environments where Sigrid CI is used.
            targetPattern = re.compile("(" + "|".join(Report.METRICS) + "):\s*([\d\.]+)", re.IGNORECASE)
            for line in open(configFile, "r"):
                match = targetPattern.match(line.strip())
                if match:
                    self.ratings[match.group(1).upper()] = float(match.group(2))
    
    def meetsTargetQualityForMetric(self, feedback, metric):
        value = feedback["newCodeRatings"].get(metric, None)
        targetRating = self.ratings.get(metric, None)
        return value == None or targetRating == None or value >= targetRating
        
    def meetsOverallQualityTarget(self, feedback):
        return all(self.meetsTargetQualityForMetric(feedback, metric) for metric in self.ratings)


class SigridApiClient:
    PROTOCOL_VERSION = "v1"
    POLL_INTERVAL = 60
    POLL_ATTEMPTS = 60
    RETRY_ATTEMPTS = 5

    def __init__(self, args):
        self.baseURL = args.sigridurl
        self.urlPartnerName = urllib.parse.quote_plus(args.partner.lower())
        self.urlCustomerName = urllib.parse.quote_plus(args.customer.lower())
        self.urlSystemName = urllib.parse.quote_plus(args.system.lower())
        self.publish = args.publish or args.publishonly
        
    def callSigridAPI(self, api, path):
        url = f"{self.baseURL}/rest/{api}{path}"
        request = urllib.request.Request(url, None)
        request.add_header("Accept", "application/json")
        request.add_header("Authorization", self.getTokenHeaderValue())
            
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        #ctx.verify_mode = ssl.CERT_NONE
        ctx.load_verify_locations("sigridci/sigridci/sigrid-says.pem")
        print (certifi.where())
        response = urllib.request.urlopen(request, context=ctx)
        # response = urllib.request.urlopen(request)
        if response.status == 204:
            return {}
        responseBody = response.read().decode("utf8")
        if len(responseBody) == 0:
            log("Received empty response")
            return {}
        return json.loads(responseBody)
        
    def getTokenHeaderValue(self):
        token = os.environ["SIGRID_CI_TOKEN"]
        if len(token) >= 32:
            return f"Bearer {token}".encode("utf8")
        else:
            account = os.environ["SIGRID_CI_ACCOUNT"]
            return b"Basic " + base64.standard_b64encode(f"{account}:{token}".encode("utf8"))

    def submitUpload(self, options, systemExists):
        log("Creating upload")
        uploadPacker = SystemUploadPacker(options)
        upload = "sigrid-upload-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".zip"
        uploadPacker.prepareUpload(options.sourceDir, upload)
    
        log("Preparing upload")
        uploadLocation = self.obtainUploadLocation(systemExists)
        uploadUrl = uploadLocation["uploadUrl"]
        analysisId = uploadLocation["ciRunId"]
        log(f"Sigrid CI analysis ID: {analysisId}")
        log("Publishing upload" if self.publish else "Submitting upload")

        if not self.uploadBinaryFile(uploadUrl, upload):
            raise Exception("Uploading file failed")
            
        return analysisId
        
    def obtainUploadLocation(self, systemExists):
        for attempt in range(self.RETRY_ATTEMPTS):
            try:
                return self.callSigridAPI("inboundresults", self.getRequestUploadPath(systemExists))
            except urllib.error.HTTPError as e:
                if e.code == 502:
                    log("Retrying")
                    time.sleep(self.POLL_INTERVAL)
                else:
                    self.processHttpError(e)
                    
        log("Sigrid is currently unavailable")
        sys.exit(1)
        
    def getRequestUploadPath(self, systemExists):
        path = f"/{self.urlPartnerName}/{self.urlCustomerName}/{self.urlSystemName}/ci/uploads/{self.PROTOCOL_VERSION}"
        if not systemExists:
            path += "/onboarding"
        elif self.publish:
            path += "/publish"
        return path
        
    def uploadBinaryFile(self, url, upload):
        with open(upload, "rb") as uploadRef:
            uploadRequest = urllib.request.Request(url, data=uploadRef.read())
            uploadRequest.method = "PUT"
            uploadRequest.add_header("Content-Type", "application/zip")
            uploadRequest.add_header("Content-Length", "%d" % os.path.getsize(upload))
            uploadRequest.add_header("x-amz-server-side-encryption", "AES256")

            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            #ctx.verify_mode = ssl.CERT_NONE
            ctx.load_verify_locations("sigridci/sigridci/consolidated.pem")
            print (certifi.where())
            uploadResponse = urllib.request.urlopen(uploadRequest, context=ctx)
            # uploadResponse = urllib.request.urlopen(uploadRequest)
            return uploadResponse.status in [200, 201, 202]
            
    def checkSystemExists(self):
        for attempt in range(self.RETRY_ATTEMPTS):
            try:
                self.callSigridAPI("analysis-results", \
                    f"/sigridci/{self.urlCustomerName}/{self.urlSystemName}/{self.PROTOCOL_VERSION}/ci")
                return True
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return False
                elif e.code == 502:
                    log("Retrying")
                    time.sleep(self.POLL_INTERVAL)
                else:
                    self.processHttpError(e)
                    
        log("Sigrid is currently unavailable")
        sys.exit(1)
            
        
    def fetchAnalysisResults(self, analysisId):
        for attempt in range(self.POLL_ATTEMPTS):
            try:
                response = self.callSigridAPI("analysis-results",
                    f"/sigridci/{self.urlCustomerName}/{self.urlSystemName}/{self.PROTOCOL_VERSION}/ci/results/{analysisId}")
                if response != {}:
                    return response            
            except urllib.error.HTTPError as e:
                self.processHttpError(e)
            except json.JSONDecodeError as e:
                log("Received incomplete analysis results")
            
            log("Waiting for analysis results")
            time.sleep(self.POLL_INTERVAL)
            
        log("Analysis failed: waiting for analysis results took too long")
        sys.exit(1)
        
    def processHttpError(self, e):
        if e.code in [401, 403]:
            log("You are not authorized to access Sigrid for this system")
            sys.exit(1)
        elif e.code == 404:
            log("Analysis results not yet available")
        elif e.code >= 500:
            log(f"Sigrid is currently not available (HTTP status {e.code})")
            sys.exit(1)
        else:      
            raise Exception(f"Received HTTP status {e.code}")
        

class SystemUploadPacker:
    MAX_UPLOAD_SIZE_MB = 500

    DEFAULT_EXCLUDES = [
        "$tf/",
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
    
    def __init__(self, options):
        self.excludePatterns = [] + (options.excludePatterns or []) + self.DEFAULT_EXCLUDES
        self.excludePatterns = [excl for excl in self.excludePatterns if excl != ""]
        if not options.includeHistory:
            self.excludePatterns += [".git/", ".gitmodules"]

        self.pathPrefix = options.pathPrefix.strip("/")
        self.showContents = options.showContents

    def prepareUpload(self, sourceDir, outputFile):
        zipFile = zipfile.ZipFile(outputFile, "w", zipfile.ZIP_DEFLATED)
        
        for root, dirs, files in os.walk(sourceDir):
            for file in sorted(files):
                filePath = os.path.join(root, file)
                if file != outputFile and not self.isExcluded(filePath):
                    relativePath = os.path.relpath(os.path.join(root, file), sourceDir)
                    uploadPath = self.getUploadFilePath(relativePath)
                    if self.showContents:
                        log(f"Adding file to upload: {uploadPath}")
                    zipFile.write(filePath, uploadPath)
        
        zipFile.close()
        
        self.checkUploadContents(outputFile)
        
    def checkUploadContents(self, outputFile):
        uploadSizeBytes = os.path.getsize(outputFile)
        uploadSizeMB = max(round(uploadSizeBytes / 1024 / 1024), 1)
        log(f"Upload size is {uploadSizeMB} MB")
        
        if uploadSizeMB > self.MAX_UPLOAD_SIZE_MB:
            raise Exception(f"Upload exceeds maximum size of {self.MAX_UPLOAD_SIZE_MB} MB")
            
        if uploadSizeBytes < 50000:
            log("Warning: Upload is very small, source directory might not contain all source code")
            
    def getUploadFilePath(self, relativePath):
        if self.pathPrefix == "":
            return relativePath
        return f"{self.pathPrefix}/{relativePath}"
        
    def isExcluded(self, filePath):
        normalizedPath = filePath.replace("\\", "/")
        for exclude in self.excludePatterns:
            if exclude.strip() in normalizedPath:
                return True
        return False
        
        
class Report:
    METRICS = ["VOLUME", "DUPLICATION", "UNIT_SIZE", "UNIT_COMPLEXITY", "UNIT_INTERFACING", "MODULE_COUPLING",
               "COMPONENT_BALANCE_PROP", "COMPONENT_INDEPENDENCE", "COMPONENT_ENTANGLEMENT", "MAINTAINABILITY"]
               
    REFACTORING_CANDIDATE_METRICS = ["DUPLICATION", "UNIT_SIZE", "UNIT_COMPLEXITY", "UNIT_INTERFACING",
                                     "MODULE_COUPLING"]

    def generate(self, feedback, args, target):
        pass
        
    def formatMetricName(self, metric):
        return metric.replace("_PROP", "").title().replace("_", " ")
        
    def formatRating(self, ratings, metric, naText="N/A"):
        if ratings.get(metric, None) == None:
            return naText
        return "%.1f" % ratings[metric]
        
    def formatBaseline(self, feedback):
        if not feedback.get("baseline", None):
            return "N/A"
        snapshotDate = datetime.datetime.strptime(feedback["baseline"], "%Y%m%d")
        return snapshotDate.strftime("%Y-%m-%d")
        
    def getSigridUrl(self, args):
        return "https://sigrid-says.com/" + urllib.parse.quote_plus(args.customer) + "/" + \
            urllib.parse.quote_plus(args.system);
            
    def getRefactoringCandidates(self, feedback, metric):
        refactoringCandidates = feedback.get("refactoringCandidates", [])
        return [rc for rc in refactoringCandidates if rc["metric"] == metric]


class TextReport(Report):
    ANSI_BOLD = "\033[1m"
    ANSI_GREEN = "\033[92m"
    ANSI_YELLOW = "\033[33m"
    ANSI_RED = "\033[91m"
    ANSI_BLUE = "\033[96m"
    LINE_WIDTH = 89
    
    def __init__(self, output=sys.stdout):
        self.output = output

    def generate(self, feedback, args, target):
        self.printHeader("Refactoring candidates")
        for metric in self.REFACTORING_CANDIDATE_METRICS:
            self.printMetric(feedback, metric)
            
        self.printHeader("Maintainability ratings")
        self.printTableRow(["System property", f"Baseline on {self.formatBaseline(feedback)}", \
            "New/changed code", "Target", "Overall" if args.publish else ""] )
        
        for metric in self.METRICS:
            if metric == "MAINTAINABILITY":
                self.printSeparator()
            
            row = [
                self.formatMetricName(metric), 
                "(" + self.formatRating(feedback["baselineRatings"], metric) + ")",
                self.formatRating(feedback["newCodeRatings"], metric),
                str(target.ratings.get(metric, "")),
                self.formatRating(feedback["baselineRatings"], metric) if args.publish else ""
            ]
        
            self.printTableRow(row, self.getRatingColor(feedback, target, metric))
            
    def printTableRow(self, row, color=None):
        formattedRow = "%-27s%-25s%-20s%-10s%-7s" % tuple(row)
        if color:
            self.printColor(formattedRow, color)
        else:
            print(formattedRow, file=self.output)
                
    def printHeader(self, header):
        print("", file=self.output)
        self.printSeparator()
        print(header, file=self.output)
        self.printSeparator()
        
    def printSeparator(self):
        print("-" * self.LINE_WIDTH, file=self.output)
                
    def printMetric(self, feedback, metric):
        print("", file=self.output)
        print(self.formatMetricName(metric), file=self.output)
        
        refactoringCandidates = self.getRefactoringCandidates(feedback, metric)
        if len(refactoringCandidates) == 0:
            print("    None", file=self.output)
        else:
            for rc in refactoringCandidates:
                print(self.formatRefactoringCandidate(rc), file=self.output)
                
    def getRatingColor(self, feedback, target, metric):
        if feedback["newCodeRatings"].get(metric, None) == None or not metric in target.ratings:
            return self.ANSI_BLUE
        elif target.meetsTargetQualityForMetric(feedback, metric):
            return self.ANSI_GREEN
        else:
            return self.ANSI_RED
                
    def formatRefactoringCandidate(self, rc):
        category = ("(" + rc["category"] + ")").ljust(14)
        subject = rc["subject"].replace("\n", "\n" + (" " * 21)).replace("::", "\n" + (" " * 21))
        return f"    - {category} {subject}"

    def printColor(self, message, ansiPrefix):
        print(ansiPrefix + message + "\033[0m", file=self.output)
        
        
class StaticHtmlReport(Report):
    HTML_STAR_FULL = "&#9733;"
    HTML_STAR_EMPTY = "&#9734;"

    def generate(self, feedback, args, target):
        if not os.path.exists("sigrid-ci-output"):
            os.mkdir("sigrid-ci-output")
    
        with open(os.path.dirname(__file__) + "/sigridci-feedback-template.html", encoding="utf-8", mode="r") as templateRef:
            template = templateRef.read()
            template = self.renderHtmlFeedback(template, feedback, args, target)

        reportFile = os.path.abspath("sigrid-ci-output/index.html")
        writer = open(reportFile, encoding="utf-8", mode="w")
        writer.write(template)
        writer.close()
        
        print("")
        print("You can find the full results here:")
        print("    " + reportFile)
        print("")
        print("You can find more information about these results in Sigrid:")
        print("    " + self.getSigridUrl(args))
        print("")
        
    def renderHtmlFeedback(self, template, feedback, args, target):
        placeholders = {
            "CUSTOMER" : html.escape(args.customer),
            "SYSTEM" : html.escape(args.system),
            "TARGET" : "%.1f" % target.ratings["MAINTAINABILITY"],
            "LINES_OF_CODE_TOUCHED" : "%d" % feedback.get("newCodeLinesOfCode", 0),
            "BASELINE_DATE" : self.formatBaseline(feedback),
            "SIGRID_LINK" : self.getSigridUrl(args),
            "MAINTAINABILITY_PASSED" : ("passed" if target.meetsOverallQualityTarget(feedback) else "failed")
        }
        
        for metric in self.METRICS:
            placeholders[f"{metric}_OVERALL"] = self.formatRating(feedback["baselineRatings"], metric)
            placeholders[f"{metric}_NEW"] = self.formatRating(feedback["newCodeRatings"], metric)
            placeholders[f"{metric}_TARGET"] = self.formatRating(target.ratings, metric, "")
            placeholders[f"{metric}_STARS_OVERALL"] = self.formatHtmlStars(feedback["baselineRatings"], metric)
            placeholders[f"{metric}_STARS_NEW"] = self.formatHtmlStars(feedback["newCodeRatings"], metric)
            placeholders[f"{metric}_PASSED"] = self.formatPassed(feedback, target, metric)
            placeholders[f"{metric}_REFACTORING_CANDIDATES"] = self.formatRefactoringCandidates(feedback, metric)
        
        return self.fillPlaceholders(template, placeholders)
        
    def fillPlaceholders(self, template, placeholders):
        for placeholder, value in placeholders.items():
            template = template.replace(f"@@@{placeholder}", value)
        return template
        
    def formatPassed(self, feedback, target, metric):
        if target.ratings.get(metric, None) == None:
            return ""
        return "passed" if target.meetsTargetQualityForMetric(feedback, metric) else "failed"
        
    def formatRefactoringCandidates(self, feedback, metric):
        refactoringCandidates = self.getRefactoringCandidates(feedback, metric)
        if len(refactoringCandidates) == 0:
            return "None"
        return "\n".join([self.formatRefactoringCandidate(rc) for rc in refactoringCandidates])
        
    def formatRefactoringCandidate(self, rc):
        subjectName = html.escape(rc["subject"]).replace("\n", "<br />").replace("::", "<br />")
        category = html.escape(rc["category"])
        return f"<span><em>({category})</em><div>{subjectName}</div></span>"
        
    def formatHtmlStars(self, ratings, metric):
        if ratings.get(metric, None) == None:
            return "N/A"
        stars = min(int(ratings[metric] + 0.5), 5)
        fullStars = stars * self.HTML_STAR_FULL
        emptyStars = (5 - stars) * self.HTML_STAR_EMPTY
        rating = self.formatRating(ratings, metric)
        return f"<strong class=\"stars{stars}\">{fullStars}{emptyStars}</strong> &nbsp; " + rating
        
        
class ExitCodeReport(Report):   
    def generate(self, feedback, args, target):
        asciiArt = TextReport()
        
        if target.meetsOverallQualityTarget(feedback):
            asciiArt.printColor("\n** SIGRID CI RUN COMPLETE: YOU WROTE MAINTAINABLE CODE AND REACHED THE TARGET **\n", \
                asciiArt.ANSI_BOLD + asciiArt.ANSI_GREEN)
        else:
            asciiArt.printColor("\n** SIGRID CI RUN COMPLETE: THE CODE YOU WROTE DID NOT MEET THE TARGET FOR MAINTAINABLE CODE **\n", \
                asciiArt.ANSI_BOLD + asciiArt.ANSI_YELLOW)
            
            # If you publish(only) we never break the build
            # We can break the build when running on a branch or pull request.
            if not args.publish:
                sys.exit(1)
                
                
class SigridCiRunner:
    def run(self, apiClient, options, target, reports):
        systemExists = apiClient.checkSystemExists()
        log("Found system in Sigrid" if systemExists else "System is not yet on-boarded to Sigrid")
        analysisId = apiClient.submitUpload(options, systemExists)

        if not systemExists:
            log(f"System '{apiClient.urlSystemName}' is on-boarded to Sigrid, and will appear in sigrid-says.com shortly")
        elif options.publishOnly:
            log("Your project's source code has been published to Sigrid")
        else:
            feedback = apiClient.fetchAnalysisResults(analysisId)
            
            if not os.path.exists("sigrid-ci-output"):
                os.mkdir("sigrid-ci-output")
            
            for report in reports:
                report.generate(feedback, args, target)
                
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--partner", type=str, default="sig")
    parser.add_argument("--customer", type=str)
    parser.add_argument("--system", type=str)
    parser.add_argument("--source", type=str)
    parser.add_argument("--targetquality", type=float, default=3.5)
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--publishonly", action="store_true")
    parser.add_argument("--exclude", type=str, default="")
    parser.add_argument("--pathprefix", type=str, default="")
    parser.add_argument("--showupload", action="store_true")
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com")
    args = parser.parse_args()
    
    if args.customer == None or args.system == None or args.source == None:
        parser.print_help()
        sys.exit(1)
    
    if sys.version_info.major == 2 or sys.version_info.minor < 7:
        print("Sigrid CI requires Python 3.7 or higher")
        sys.exit(1)
        
    if not "SIGRID_CI_TOKEN" in os.environ:
        print("Missing required environment variable SIGRID_CI_TOKEN")
        sys.exit(1)
        
    if not os.path.exists(args.source):
        print("Source code directory not found: " + args.source)
        sys.exit(1)
        
    if args.publish and len(args.pathprefix) > 0:
        print("You cannot use both --publish and --pathprefix at the same time, refer to the documentation for details")
        sys.exit(1)

    if not SYSTEM_NAME_PATTERN.match(args.system):
        print("Invalid system name, system name can only contain letters/numbers/hyphens, and cannot start with a hyphen")
        sys.exit(1)

    log("Starting Sigrid CI")
    options = UploadOptions(args.source, args.exclude.split(","), args.history, args.pathprefix, args.showupload, args.publishonly)
    target = TargetQuality(f"{args.source}/sigrid.yaml", args.targetquality)
    apiClient = SigridApiClient(args)
    reports = [TextReport(), StaticHtmlReport(), ExitCodeReport()]
    
    runner = SigridCiRunner()
    runner.run(apiClient, options, target, reports)
