import os
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.github_pull_request_report import GitHubPullRequestReport
from sigridci.sigridci.reports.maintainability_markdown_report import MaintainabilityMarkdownReport

options = PublishOptions("sig", "demo-system", RunMode.FEEDBACK_ONLY, outputDir="/tmp/fb")
feedback = {
    "baseline": "20220110",
    "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
    "changedCodeBeforeRatings": {"MAINTAINABILITY": 2.6},
    "changedCodeAfterRatings": {"MAINTAINABILITY": 2.8},
    "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 4.0},
    "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
    "refactoringCandidates": [],
}
GitHubPullRequestReport(MaintainabilityMarkdownReport()).generate("1234", feedback, options)