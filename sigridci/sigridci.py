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
import dataclasses
import datetime
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import typing
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from xml.dom import minidom

LOG_HISTORY = []


def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}  {message}", flush=True)
    LOG_HISTORY.append(message)


@dataclass
class UploadOptions:
    source_dir: str = None
    exclude_patterns: typing.List[str] = dataclasses.field(default_factory=lambda: [])
    include_history: bool = False
    subsystem: str = ""
    show_contents: bool = False
    publish_only: bool = False
    
    def read_scope_file(self):
        return self.locate_file(["sigrid.yaml", "sigrid.yml"])
        
    def read_metadata_file(self):
        return self.locate_file(["sigrid-metadata.yaml", "sigrid-metadata.yml"])
    
    def locate_file(self, possible_file_names):
        for file in possible_file_names:
            if os.path.exists(f"{self.source_dir}/{file}"):
                with open(f"{self.source_dir}/{file}", "r") as f:
                    return f.read()
        return None


class TargetQuality:
    def __init__(self, scope, target_rating):
        self.ratings = {"MAINTAINABILITY" : target_rating}
        
        # We can't use pyyaml because PIP is not available in the some of the
        # very diverse set of customer environments where Sigrid CI is used.
        target_pattern = re.compile("(" + "|".join(Report.METRICS) + "):\s*([\d\.]+)", re.IGNORECASE)
        
        for line in scope.split("\n"):
            match = target_pattern.match(line.strip())
            if match:
                log(f"Loading {match.group(1).upper()} target from scope configuration file")
                self.ratings[match.group(1).upper()] = float(match.group(2))

    def meets_target_quality_for_metric(self, feedback, metric):
        value = feedback["newCodeRatings"].get(metric, None)
        target_rating = self.ratings.get(metric, None)
        return value == None or target_rating == None or value >= target_rating
        
    def meets_quality_targets(self, feedback):
        return all(self.meets_target_quality_for_metric(feedback, metric) for metric in self.ratings)


class Sigridapi_client:
    API_VERSION = "v1"
    POLL_INTERVAL = 30
    POLL_ATTEMPTS = 120

    def __init__(self, args):
        self.base_url = args.sigridurl
        self.url_partner_name = urllib.parse.quote_plus(args.partner.lower())
        self.url_customer_name = urllib.parse.quote_plus(args.customer.lower())
        self.url_system_name = urllib.parse.quote_plus(args.system.lower())
        self.publish = args.publish or args.publishonly
        self.subsystem = args.subsystem

    def call_sigrid_api(self, path, body=None, content_type=None):
        url = f"{self.base_url}/rest/{path}"
        request = urllib.request.Request(url, body)
        request.add_header("Accept", "application/json")
        request.add_header("Authorization", f"Bearer {os.environ['SIGRID_CI_TOKEN']}".encode("utf8"))
        if content_type != None:
            request.add_header("Content-Type", content_type)

        response = urllib.request.urlopen(request)
        if response.status == 204:
            return {}
        response_body = response.read().decode("utf8")
        if len(response_body) == 0:
            log("Received empty response")
            return {}
        return json.loads(response_body)
        
    def retry(self, operation, *, attempts=5, allow_404=False, allow_empty=True):
        for attempt in range(attempts):
            try:
                response = operation()
                if allow_empty or response != {}:
                    return response
            except urllib.error.HTTPError as e:
                if e.code in [401, 403]:
                    log("You are not authorized to access Sigrid for this system")
                    sys.exit(1)
                elif allow_404 and e.code == 404:
                    return False
            
            # These statements are intentionally outside of the except-block,
            # since we want to retry for empty response on some end points.
            log("Retrying")
            time.sleep(self.POLL_INTERVAL)
        
        log(f"Sigrid is currently unavailable, failed after {attempts} attempts")
        sys.exit(1)

    def submit_upload(self, options, system_exists):
        with tempfile.TemporaryDirectory() as tempDir:
            log("Creating upload")
            upload_packer = SystemUploadPacker(options)
            upload = os.path.join(tempDir, "upload.zip")
            upload_packer.prepare_upload(options.source_dir, upload)

            log("Preparing upload")
            upload_location = self.obtain_upload_location(system_exists)
            upload_url = upload_location["upload_url"]
            analysis_id = upload_location["ciRunId"]
            log(f"Sigrid CI analysis ID: {analysis_id}")
            log("Publishing upload" if self.publish else "Submitting upload")
            self.upload_binary_file(upload_url, upload)

            return analysis_id

    def obtain_upload_location(self, system_exists):
        path = f"/inboundresults/{self.url_partner_name}/{self.url_customer_name}/{self.url_system_name}/ci/uploads/{self.API_VERSION}"
        if not system_exists:
            path += "/onboarding"
        elif self.publish:
            path += "/publish"
        if self.subsystem:
            path += "?subsystem=" + urllib.parse.quote_plus(self.subsystem)
    
        return self.retry(lambda: self.call_sigrid_api(path))
        
    def validate_scope_file(self, scopeFile):
        path = f"/inboundresults/{self.url_partner_name}/{self.url_customer_name}/{self.url_system_name}/ci/validate/{self.API_VERSION}"
        return self.retry(lambda: self.call_sigrid_api(path, scopeFile.encode("utf8"), "application/yaml"))
        
    def validate_metadata(self, metadataFile):
        path = f"/analysis-results/sigridci/{self.url_customer_name}/validate"
        return self.retry(lambda: self.call_sigrid_api(path, metadataFile.encode("utf8"), "application/yaml"))

    def upload_binary_file(self, url, upload):
        self.retry(lambda: self.attempt_upload(url, upload))
        log(f"Upload successful")

    def attempt_upload(self, url, upload):
        with open(upload, "rb") as uploadRef:
            upload_request = urllib.request.Request(url, data=uploadRef)
            upload_request.method = "PUT"
            upload_request.add_header("Content-Type", "application/zip")
            upload_request.add_header("Content-Length", "%d" % os.path.getsize(upload))
            upload_request.add_header("x-amz-server-side-encryption", "AES256")
            urllib.request.urlopen(upload_request)

    def check_system_exists(self):
        path = f"/analysis-results/sigridci/{self.url_customer_name}/{self.url_system_name}/{self.API_VERSION}/ci"
        return self.retry(lambda: self.call_sigrid_api(path), allow_404=True) != False

    def fetch_analysis_results(self, analysis_id):
        log("Waiting for analysis results")
        path = f"/analysis-results/sigridci/{self.url_customer_name}/{self.url_system_name}/{self.API_VERSION}/ci/results/{analysis_id}"
        return self.retry(lambda: self.call_sigrid_api(path), attempts=self.POLL_ATTEMPTS, allow_empty=False)
        
    def fetch_metadata(self):
        path = f"/analysis-results/api/{self.API_VERSION}/system-metadata/{self.url_customer_name}/{self.url_system_name}"
        return self.retry(lambda: self.call_sigrid_api(path))
        
    def fetch_objectives(self):
        path = f"/analysis-results/api/{self.API_VERSION}/objectives/{self.url_customer_name}/{self.url_system_name}/config"
        return self.retry(lambda: self.call_sigrid_api(path))
        
    def get_landing_page(self, analysis_id, target):
        target_rating = "%.1f" % target.ratings["MAINTAINABILITY"]
        return f"{self.base_url}/{self.url_customer_name}/{self.url_system_name}/-/sigrid-ci/{analysis_id}?target_rating={target_rating}"


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
        ".git/",
        ".gitattributes",
        ".gitignore",
        ".idea/",
        ".jpg",
        ".png"
    ]

    def __init__(self, options):
        self.options = options

    def prepare_upload(self, source_dir, output_file):
        zip_file = zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED)
        has_contents = False
        
        if self.options.include_history and os.path.exists(f"{source_dir}/.git"):
            self.include_repository_history(source_dir)

        for root, dirs, files in os.walk(source_dir):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                if file != output_file and not self.is_excluded(file_path):
                    relative_path = os.path.relpath(os.path.join(root, file), source_dir)
                    has_contents = True
                    if self.options.show_contents:
                        log(f"Adding file to upload: {relative_path}")
                    zip_file.write(file_path, relative_path)

        zip_file.close()

        self.check_upload_contents(output_file, has_contents)

    def check_upload_contents(self, output_file, has_contents):
        upload_size_bytes = os.path.getsize(output_file)
        upload_size_mb = max(round(upload_size_bytes / 1024 / 1024), 1)
        log(f"Upload size is {upload_size_mb} MB")

        if upload_size_mb > self.MAX_UPLOAD_SIZE_MB:
            raise Exception(f"Upload exceeds maximum size of {self.MAX_UPLOAD_SIZE_MB} MB")
        elif not has_contents:
            print(f"No code found to upload, please check the directory used for --source")
            sys.exit(1)
        elif upload_size_bytes < 50000:
            log("Warning: Upload is very small, source directory might not contain all source code")

    def is_excluded(self, file_path):
        exclude_patterns = self.DEFAULT_EXCLUDES + (self.options.exclude_patterns or [])
        normalized_path = file_path.replace("\\", "/")
        for exclude in exclude_patterns:
            if exclude != "" and exclude.strip() in normalized_path:
                return True
        return False
        
    def include_repository_history(self, source_dir):
        git_command = ["git", "-C", source_dir, "--no-pager", "log", "--date=iso", "--format='@@@;%H;%an;%ae;%ad;%s'", \
                      "--numstat", "--no-merges"]
        try:
            output = subprocess.run(git_command, stdout=subprocess.PIPE)
            if output.returncode == 0:
                with open(f"{source_dir}/git.log", "w") as f:
                    f.write(output.stdout.decode("utf8"))
            else:
                log("Exporting repository history failed")
        except Exception as e:
            log("Error while trying to include repository history: " + str(e))
    

class Report:
    METRICS = ["VOLUME", "DUPLICATION", "UNIT_SIZE", "UNIT_COMPLEXITY", "UNIT_INTERFACING", "MODULE_COUPLING",
               "COMPONENT_BALANCE_PROP", "COMPONENT_INDEPENDENCE", "COMPONENT_ENTANGLEMENT", "MAINTAINABILITY"]

    REFACTORING_CANDIDATE_METRICS = ["DUPLICATION", "UNIT_SIZE", "UNIT_COMPLEXITY", "UNIT_INTERFACING",
                                     "MODULE_COUPLING"]

    def generate(self, analysis_id, feedback, args, target):
        pass

    def format_metric_name(self, metric):
        return metric.replace("_PROP", "").title().replace("_", " ")

    def format_rating(self, ratings, metric, naText="N/A"):
        if ratings.get(metric, None) == None:
            return naText
        return "%.1f" % ratings[metric]

    def format_baseline(self, feedback):
        if not feedback.get("baseline", None):
            return "N/A"
        snapshot_date = datetime.datetime.strptime(feedback["baseline"], "%Y%m%d")
        return snapshot_date.strftime("%Y-%m-%d")

    def get_sigrid_url(self, args):
        customer = urllib.parse.quote_plus(args.customer.lower())
        system = urllib.parse.quote_plus(args.system.lower())
        return f"https://sigrid-says.com/{customer}/{system}"

    def get_refactoring_candidates(self, feedback, metric):
        refactoring_candidates = feedback.get("refactoringCandidates", [])
        return [rc for rc in refactoring_candidates if rc["metric"] == metric or metric == "MAINTAINABILITY"]


class TextReport(Report):
    ANSI_BOLD = "\033[1m"
    ANSI_GREEN = "\033[92m"
    ANSI_YELLOW = "\033[33m"
    ANSI_RED = "\033[91m"
    ANSI_BLUE = "\033[96m"
    LINE_WIDTH = 89

    def __init__(self, output=sys.stdout):
        self.output = output

    def generate(self, analysis_id, feedback, args, target):
        self.print_header("Refactoring candidates")
        for metric in self.REFACTORING_CANDIDATE_METRICS:
            self.print_metric(feedback, metric)

        self.print_header("Maintainability ratings")
        self.print_table_row(["System property", f"Baseline on {self.format_baseline(feedback)}", \
            "New/changed code", "Target", "Overall" if args.publish else ""])

        for metric in self.METRICS:
            if metric == "MAINTAINABILITY":
                self.print_separator()

            row = [
                self.format_metric_name(metric),
                "(" + self.format_rating(feedback["baselineRatings"], metric) + ")",
                self.format_rating(feedback["newCodeRatings"], metric),
                str(target.ratings.get(metric, "")),
                self.format_rating(feedback["baselineRatings"], metric) if args.publish else ""
            ]

            self.print_table_row(row, self.get_rating_color(feedback, target, metric))

    def print_table_row(self, row, color=None):
        formatted_row = "%-27s%-25s%-20s%-10s%-7s" % tuple(row)
        if color:
            self.print_color(formatted_row, color)
        else:
            print(formatted_row, file=self.output)

    def print_header(self, header):
        print("", file=self.output)
        self.print_separator()
        print(header, file=self.output)
        self.print_separator()

    def print_separator(self):
        print("-" * self.LINE_WIDTH, file=self.output)

    def print_metric(self, feedback, metric):
        print("", file=self.output)
        print(self.format_metric_name(metric), file=self.output)

        refactoring_candidates = self.get_refactoring_candidates(feedback, metric)
        if len(refactoring_candidates) == 0:
            print("    None", file=self.output)
        else:
            for rc in refactoring_candidates:
                print(self.format_refactoring_candidate(rc), file=self.output)

    def get_rating_color(self, feedback, target, metric):
        if feedback["newCodeRatings"].get(metric, None) == None or not metric in target.ratings:
            return self.ANSI_BLUE
        elif target.meets_target_quality_for_metric(feedback, metric):
            return self.ANSI_GREEN
        else:
            return self.ANSI_RED

    def format_refactoring_candidate(self, rc):
        category = ("(" + rc["category"] + ")").ljust(14)
        subject = rc["subject"].replace("\n", "\n" + (" " * 21)).replace("::", "\n" + (" " * 21))
        return f"    - {category} {subject}"

    def print_color(self, message, ansi_prefix):
        print(ansi_prefix + message + "\033[0m", file=self.output)


class StaticHtmlReport(Report):
    HTML_STAR_FULL = "&#9733;"
    HTML_STAR_EMPTY = "&#9734;"

    def generate(self, analysis_id, feedback, args, target):
        with open(os.path.dirname(__file__) + "/sigridci-feedback-template.html", encoding="utf-8", mode="r") as templateRef:
            template = templateRef.read()
            template = self.render_html_feedback(template, feedback, args, target)

        report_file = os.path.abspath("sigrid-ci-output/index.html")
        writer = open(report_file, encoding="utf-8", mode="w")
        writer.write(template)
        writer.close()

        print("")
        print("You can find the full results here:")
        print("    " + report_file)
        print("")
        print("You can find more information about these results in Sigrid:")
        print("    " + self.get_sigrid_url(args))
        print("")

    def render_html_feedback(self, template, feedback, args, target):
        placeholders = {
            "CUSTOMER" : html.escape(args.customer),
            "SYSTEM" : html.escape(args.system),
            "TARGET" : "%.1f" % target.ratings["MAINTAINABILITY"],
            "LINES_OF_CODE_TOUCHED" : "%d" % feedback.get("newCodeLinesOfCode", 0),
            "BASELINE_DATE" : self.format_baseline(feedback),
            "SIGRID_LINK" : self.get_sigrid_url(args),
            "MAINTAINABILITY_PASSED" : ("passed" if target.meets_quality_targets(feedback) else "failed")
        }

        for metric in self.METRICS:
            placeholders[f"{metric}_OVERALL"] = self.format_rating(feedback["baselineRatings"], metric)
            placeholders[f"{metric}_NEW"] = self.format_rating(feedback["newCodeRatings"], metric)
            placeholders[f"{metric}_TARGET"] = self.format_rating(target.ratings, metric, "")
            placeholders[f"{metric}_STARS_OVERALL"] = self.format_html_stars(feedback["baselineRatings"], metric)
            placeholders[f"{metric}_STARS_NEW"] = self.format_html_stars(feedback["newCodeRatings"], metric)
            placeholders[f"{metric}_PASSED"] = self.format_passed(feedback, target, metric)
            placeholders[f"{metric}_REFACTORING_CANDIDATES"] = self.format_refactoring_candidates(feedback, metric)

        return self.fill_placeholders(template, placeholders)

    def fill_placeholders(self, template, placeholders):
        for placeholder, value in placeholders.items():
            template = template.replace(f"@@@{placeholder}", value)
        return template

    def format_passed(self, feedback, target, metric):
        if target.ratings.get(metric, None) == None:
            return ""
        return "passed" if target.meets_target_quality_for_metric(feedback, metric) else "failed"

    def format_refactoring_candidates(self, feedback, metric):
        refactoring_candidates = self.get_refactoring_candidates(feedback, metric)
        if len(refactoring_candidates) == 0:
            return "None"
        return "\n".join([self.format_refactoring_candidate(rc) for rc in refactoring_candidates])

    def format_refactoring_candidate(self, rc):
        subject_name = html.escape(rc["subject"]).replace("\n", "<br />").replace("::", "<br />")
        category = html.escape(rc["category"])
        return f"<span><em>({category})</em><div>{subject_name}</div></span>"

    def format_html_stars(self, ratings, metric):
        if ratings.get(metric, None) == None:
            return "N/A"
        stars = min(int(ratings[metric] + 0.5), 5)
        full_stars = stars * self.HTML_STAR_FULL
        empty_stars = (5 - stars) * self.HTML_STAR_EMPTY
        rating = self.format_rating(ratings, metric)
        return f"<strong class=\"stars{stars}\">{full_stars}{empty_stars}</strong> &nbsp; " + rating


class JUnitFormatReport(Report):
    def generate(self, analysis_id, feedback, args, target):
        with open("sigrid-ci-output/sigridci-junit-format-report.xml", "w") as fileRef:
            fileRef.write(self.generate_xml(feedback, target))

    def generate_xml(self, feedback, target):
        dom = minidom.Document()
        test_suite = dom.createElement("testsuite")
        test_suite.setAttribute("name", "Sigrid CI")
        dom.appendChild(test_suite)

        test_case = dom.createElement("testcase")
        test_case.setAttribute("classname", "Sigrid CI")
        test_case.setAttribute("name", "Maintainability")
        test_suite.appendChild(test_case)

        failures = self.get_failures(feedback, target)
        if len(failures) > 0:
            failure = dom.createElement("failure")
            failure.appendChild(dom.createTextNode("Refactoring candidates:\n\n" + "\n".join(failures)))
            test_case.appendChild(failure)

        return dom.toprettyxml(indent="    ")

    def get_failures(self, feedback, target):
        if target.meets_quality_targets(feedback):
            return []

        format_failure = lambda rc: f"- {rc['subject']}\n  ({self.format_metric_name(rc['metric'])}, {rc['category']})"

        candidates = self.get_refactoring_candidates(feedback, "MAINTAINABILITY")\
            if not target.meets_target_quality_for_metric(feedback, "MAINTAINABILITY")\
            else self.get_failed_rcs(feedback, target)
        return [format_failure(rc) for rc in candidates]

    def get_failed_rcs(self, feedback, target):
        lists = [self.get_refactoring_candidates(feedback, m) for m in target.ratings
                 if not target.meets_target_quality_for_metric(feedback, m)]
        return [item for sublist in lists for item in sublist]
                
                
class ConclusionReport(Report):
    def __init__(self, api_client, output=sys.stdout):
        self.api_client = api_client
        self.output = output

    def generate(self, analysis_id, feedback, args, target):
        self.print_conclusion_message(feedback, target)
        self.print_landing_page(analysis_id, feedback, target)
        # If you publish(only) we never break the build
        # We can break the build when running on a branch or pull request.
        if not target.meets_quality_targets(feedback) and not args.publish:
            sys.exit(1)
            
    def print_conclusion_message(self, feedback, target):
        ascii_art = TextReport(self.output)

        if feedback["newCodeRatings"].get("MAINTAINABILITY", None) == None:
            ascii_art.print_color("\n** SIGRID CI RUN COMPLETE: NO FILES CONSIDERED FOR MAINTAINABILITY WERE CHANGED **\n", \
                                 ascii_art.ANSI_BOLD + ascii_art.ANSI_BLUE)
        elif target.meets_quality_targets(feedback):
            ascii_art.print_color("\n** SIGRID CI RUN COMPLETE: YOU WROTE MAINTAINABLE CODE AND REACHED THE TARGET **\n", \
                                 ascii_art.ANSI_BOLD + ascii_art.ANSI_GREEN)
        else:
            ascii_art.print_color("\n** SIGRID CI RUN COMPLETE: THE CODE YOU WROTE DID NOT MEET THE TARGET FOR MAINTAINABLE CODE **\n", \
                                 ascii_art.ANSI_BOLD + ascii_art.ANSI_YELLOW)
                
    def print_landing_page(self, analysis_id, feedback, target):
        landing_page = self.api_client.get_landing_page(analysis_id, target)
        
        print("", file=self.output)
        print("-" * (len(landing_page) + 4), file=self.output)
        print("View your analysis results in Sigrid:", file=self.output)
        print(f"    {landing_page}", file=self.output)
        print("-" * (len(landing_page) + 4), file=self.output)
        print("", file=self.output)


class SigridCiRunner:
    SYSTEM_NAME_PATTERN = re.compile("^[a-z0-9]+(-[a-z0-9]+)*$", re.IGNORECASE)
    SYSTEM_NAME_LENGTH = range(2, 65)
    METADATA_FIELDS = [
        "displayName",
        "divisionName",
        "teamNames",
        "supplierNames",
        "lifecyclePhase",
        "inProductionSince",
        "businessCriticality",
        "targetIndustry",
        "deploymentType",
        "applicationType",
        "externalID",
        "isDevelopmentOnly",
        "remark"
    ]
    
    def load_sigrid_target(self, api_client):
        objectives = api_client.fetch_objectives()
        target_rating = objectives.get("NEW_CODE_QUALITY", objectives.get("MAINTAINABILITY", 3.5))
        log("Using Sigrid for target rating (%.1f stars)" % target_rating)
        return target_rating

    def run(self, api_client, options, target, reports):
        if os.path.exists(f"{options.source_dir}/sigrid.yml"):
            log("Found sigrid.yml in repository. Did you mean sigrid.yaml?")
            sys.exit(1)
    
        system_exists = api_client.check_system_exists()
        log("Found system in Sigrid" if system_exists else "System is not yet on-boarded to Sigrid")
        
        self.prepare_metadata(options)
        self.validate_configuration_files(api_client, options)
        analysis_id = api_client.submit_upload(options, system_exists)

        if not system_exists:
            log(f"System '{api_client.url_system_name}' is on-boarded to Sigrid, and will appear in sigrid-says.com shortly")
        elif options.publish_only:
            log("Your project's source code has been published to Sigrid")
            self.display_metadata(api_client, options)
        else:
            feedback = api_client.fetch_analysis_results(analysis_id)
            self.display_metadata(api_client, options)

            if not os.path.exists("sigrid-ci-output"):
                os.mkdir("sigrid-ci-output")

            for report in reports:
                report.generate(analysis_id, feedback, args, target)
                
    def validate_configuration_files(self, api_client, options):
        scope = options.read_scope_file()
        if scope:
            self.validateConfiguration(lambda: api_client.validate_scope_file(scope), "scope configuration file")
        
        metadataFile = options.read_metadata_file()
        if metadataFile:
            self.validateConfiguration(lambda: api_client.validate_metadata(metadataFile), "Sigrid metadata file")
    
    def validateConfiguration(self, validation_call, configuration_name):
        log(f"Validating {configuration_name}")
        validation_result = validation_call()
        if validation_result["valid"]:
            log("Validation passed")
        else:
            log("-" * 80)
            log(f"Invalid {configuration_name}:")
            for note in validation_result["notes"]:
                log(f"    - {note}")
            log("-" * 80)
            sys.exit(1)
            
    def display_metadata(self, api_client, options):
        if options.read_metadata_file() == None:
            print("")
            print("Sigrid metadata for this system:")
            for key, value in api_client.fetch_metadata().items():
                if value:
                    print(f"    {key}:".ljust(20) + str(value))
                    
    def prepare_metadata(self, options):
        get_metadata_value = lambda field: os.environ.get(field.lower(), "")
        metadata = {field: get_metadata_value(field) for field in self.METADATA_FIELDS if get_metadata_value(field)}
        
        if len(metadata) > 0:
            if options.read_metadata_file() != None:
                raise Exception("Cannot add metadata using environment variables if metadata YAML file is already used")
            
            with open(f"{options.source_dir}/sigrid-metadata.yaml", "w") as writer:
                writer.write("metadata:\n")
                for name, value in metadata.items():
                    formatted_value = f"[\"{value}\"]" if name in ["teamNames", "supplierNames"] else f"\"{value}\""
                    writer.write(f"  {name}: {formatted_value}\n")
                
    def is_valid_system_name(self, customer_name, system_name):
        return self.SYSTEM_NAME_PATTERN.match(system_name) and \
            len(system_name) >= self.SYSTEM_NAME_LENGTH.start and \
            (len(system_name) + len(customer_name) + 1) in self.SYSTEM_NAME_LENGTH


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--partner", type=str, default="sig")
    parser.add_argument("--customer", type=str)
    parser.add_argument("--system", type=str)
    parser.add_argument("--source", type=str)
    parser.add_argument("--targetquality", type=str, default="sigrid")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--publishonly", action="store_true")
    parser.add_argument("--exclude", type=str, default="")
    parser.add_argument("--subsystem", type=str, default="")
    parser.add_argument("--showupload", action="store_true")
    parser.add_argument("--include-history", action="store_true")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com")
    # Dummy argument used when passing false to boolean arguments.
    # BooleanOptionalAction would solve this, but requires Python 3.9+.
    parser.add_argument("--dummy", action="store_true")
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

    log("Starting Sigrid CI")
    
    options = UploadOptions(args.source, args.exclude.split(","), args.include_history, args.subsystem, args.showupload, args.publishonly)
    api_client = Sigridapi_client(args)
    reports = [TextReport(), StaticHtmlReport(), JUnitFormatReport(), ConclusionReport(api_client)]

    runner = SigridCiRunner()
    
    if not runner.is_valid_system_name(args.customer, args.system):
        maxNameLength = runner.SYSTEM_NAME_LENGTH.stop - (len(args.customer) + 1)
        print(f"Invalid system name, system name should match '{runner.SYSTEM_NAME_PATTERN.pattern}' "
              f"and be {runner.SYSTEM_NAME_LENGTH.start} to {maxNameLength} characters long (inclusive).")
        sys.exit(1)
        
    target_rating = runner.load_sigrid_target(api_client) if args.targetquality == "sigrid" else float(args.targetquality)
    target = TargetQuality(options.read_scope_file() or "", target_rating)
    runner.run(api_client, options, target, reports)
