# Copyright Software Improvement Group
# Copyright Alliander N.V.
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

from unittest import TestCase

from sigridci.sigridci.capability import MAINTAINABILITY, SECURITY
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.telemetry import Telemetry


class TelemetryTest(TestCase):

    def testSendEventForMissingLicenses(self):
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, "/tmp")
        options.capabilities = [MAINTAINABILITY]

        telemetry = DummyTelemetry(options)
        telemetry.trackUnusedLicenses(["MAINTAINABILITY", "SECURITY"])

        self.assertEqual(telemetry.captured, ["sigridci.unused/security"])

    def testDoNotSendEventIfAllCapabilitiesAreUsed(self):
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, "/tmp")
        options.capabilities = [MAINTAINABILITY, SECURITY]

        telemetry = DummyTelemetry(options)
        telemetry.trackUnusedLicenses(["MAINTAINABILITY", "SECURITY"])

        self.assertEqual(telemetry.captured, [])

    def testDoNotSendEventIsNoLicense(self):
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, "/tmp")
        options.capabilities = [MAINTAINABILITY]

        telemetry = DummyTelemetry(options)
        telemetry.trackUnusedLicenses(["MAINTAINABILITY"])

        self.assertEqual(telemetry.captured, [])


class DummyTelemetry(Telemetry):
    def __init__(self, options):
        super().__init__(options)
        self.captured = []

    def sendEvent(self, category, details):
        self.captured.append(f"{category}/{details}")
