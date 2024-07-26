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

import json
import os
import sys
from datetime import date, timedelta
from http.client import RemoteDisconnected
from json import JSONDecodeError
from typing import TypedDict, Callable, Any
from urllib import request
from urllib.error import URLError
import logging
from argparse import ArgumentParser

LOG = logging.getLogger(__name__)


class Finding(TypedDict):
    href: str
    first_seen_snapshot_date: date
    file_path: str
    start_line: int
    end_line: int
    type: str
    severity: str
    severity_score: float
    status: str


class SigridApiClient:

    def __init__(self, customer: str, system: str, token: str):
        self.sigrid_api = f'https://sigrid-says.com/rest/analysis-results/api/v1/security-findings/{customer}/{system}'
        self.token = token

    def get_findings(self) -> Any | None:
        try:
            req = request.Request(self.sigrid_api)
            req.add_header('Authorization', 'Bearer ' + self.token)
            with request.urlopen(req) as response:
                return json.loads(self.handle_response(response))
        except URLError as e:
            LOG.error('Unable to connect to Sigrid API: %s', str(e))
            return None
        except RemoteDisconnected:
            LOG.error('Sigrid disconnected or timed out')
            return None
        except JSONDecodeError:
            LOG.error('Sigrid API response contains invalid JSON')
            return None

    @staticmethod
    def handle_response(response):
        if response.status == 200:
            findings = response.read().decode('utf-8')
            LOG.info('Sigrid returned findings JSON (length: %s chars)', len(findings))
            return findings
        else:
            LOG.error('Sigrid returned status code %s', response.status)
            return None

    @staticmethod
    def is_valid_token(token):
        return token is not None and len(token) >= 64


class SlackAPI:

    def __init__(self, webhook_uri: str):
        self.slack_webhook_uri = webhook_uri

    def post_message(self, message: str) -> bool:
        try:
            body = str.encode(json.dumps({'type': 'mrkdwn', 'text': message}))
            req = request.Request(self.slack_webhook_uri, body, method='POST')
            req.add_header('Content-Type', 'application/json')
            with request.urlopen(req) as response:
                return self.handle_response(response)
        except UnicodeEncodeError:
            LOG.error('message contains something that cannot be encoded in UTF-8')
            return False
        except URLError:
            LOG.error('protocol error trying to post to %s', self.slack_webhook_uri)
            return False

    @staticmethod
    def handle_response(response):
        if response.status == 200:
            LOG.info('Message posted')
            return True
        else:
            LOG.error('Calling incoming Slack webhook failed: status=%s', response.status)
            return False

    @staticmethod
    def is_valid_webhook(url):
        return url is not None and url.startswith('https://hooks.slack.com/services')


def filter_finding(finding: Finding) -> bool:
    return date.today() - finding['first_seen_snapshot_date'] < timedelta(days=8)


def process_findings(all_findings: Any, include: Callable[[Finding], bool]) -> list[Finding]:
    result = []
    for raw_finding in all_findings:
        finding: Finding = {
            'href': raw_finding['href'],
            'first_seen_snapshot_date': date.fromisoformat(raw_finding['firstSeenSnapshotDate']),
            'file_path': raw_finding['filePath'],
            'start_line': raw_finding['startLine'],
            'end_line': raw_finding['endLine'],
            'type': raw_finding['type'],
            'severity': raw_finding['severity'],
            'severity_score': raw_finding['severityScore'],
            'status': raw_finding['status']
        }
        if include(finding):
            result.append(finding)
    if len(result) == 0:
        return result
    else:
        return sorted(result, key=lambda x: (x['severity_score'], x['first_seen_snapshot_date']), reverse=True)


def get_filename(file_path: str | None) -> str:
    if not file_path:
        return ''
    else:
        if file_path.endswith('/'):
            file_path = file_path[:-1]
        parts = file_path.split('/')
        return parts[-1]


def create_message(system: str, findings: list[Finding], num_findings: int) -> str:
    if len(findings) == 0:
        message = f'No new open findings found in {args.system} in the last week! 🎉'
    else:
        message = f'{len(findings)} new open findings in _{system}_ during the last week'
    if len(findings) > 5:
        message += '. The 5 most severe ones are:\n'
    else:
        message += '.\n'
    for finding in findings[:5]:
        message += f'• [*{finding["severity"]}*, {finding["status"]}] <{finding["href"]}|{finding["type"]}> in `{get_filename(finding["file_path"])}`, '
        if finding["start_line"] != finding["end_line"]:
            message += f'lines {finding["start_line"]}-{finding["end_line"]}\n'
        else:
            message += f'line {finding["start_line"]}\n'
    if num_findings > len(findings):
        message += f'There are {num_findings - len(findings)} older open findings.'
    return message


if __name__ == "__main__":
    parser = ArgumentParser(description='Gets open security/reliability findings and post them to Slack.')
    parser.add_argument('--customer', type=str, help="Name of your organization's Sigrid account.")
    parser.add_argument('--system', type=str, help='Name of your system in Sigrid, letters/digits/hyphens only.')
    args = parser.parse_args()

    if None in [args.customer, args.system]:
        parser.print_help()
        sys.exit(1)

    if sys.version_info.major == 2 or sys.version_info.minor < 9:
        print('Sigrid CI requires Python 3.9 or higher')
        sys.exit(1)

    sigrid_authentication_token = os.getenv('SIGRID_CI_TOKEN')
    if not SigridApiClient.is_valid_token(sigrid_authentication_token):
        print('Missing or incomplete environment variable SIGRID_CI_TOKEN')
        sys.exit(1)

    slack_webhook_uri = os.getenv('SECURITY_FINDINGS_WEBHOOK')
    if not SlackAPI.is_valid_webhook(slack_webhook_uri):
        print('Missing or incomplete environment variable SECURITY_FINDINGS_WEBHOOK')
        sys.exit(1)

    logging.basicConfig(encoding='utf-8', level=logging.INFO)

    slack = SlackAPI(slack_webhook_uri)
    sigrid = SigridApiClient(args.customer, args.system, sigrid_authentication_token)
    all_findings = sigrid.get_findings()
    processed_findings = process_findings(all_findings, filter_finding)
    slack.post_message(create_message(args.system, processed_findings, len(all_findings)))
