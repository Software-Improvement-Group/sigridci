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

import urllib.parse
import urllib.request

from .capability import ALL_CAPABILITIES
from .platform import Platform
from .publish_options import RunMode
from .upload_log import UploadLog

# This file is responsible for anonymous statistics. If you want to know more about how SIG uses this data,
# see https://www.softwareimprovementgroup.com/wp-content/uploads/SIG_Sigrid_Privacy_Statement.pdf for our
# Privacy Statement.

class Telemetry:
    TIMEOUT_S = 10

    def __init__(self, options):
        self.options = options

    def trackRun(self):
        self.sendEvent("sigridci.platform", Platform.getPlatformId())

    def trackUnusedLicenses(self, licenses):
        if self.options.runMode in (RunMode.FEEDBACK_ONLY, RunMode.FEEDBACK_AND_PUBLISH):
            for capability in ALL_CAPABILITIES:
                if self.hasLicense(capability, licenses) and not self.isUsed(capability):
                    self.sendEvent("sigridci.unused", capability.shortName)

    def sendEvent(self, category, details):
        if self.options.feedbackURL:
            ec = urllib.parse.quote_plus(category)
            ea = urllib.parse.quote_plus(details)
            en = urllib.parse.quote_plus(self.options.getSystemId())

            try:
                url = f"{self.options.sigridURL}/usage/matomo.php?idsite=6&rec=1&ca=1&e_c={ec}&e_a={ea}&e_n={en}"
                request = urllib.request.Request(url)
                urllib.request.urlopen(request, None, timeout=self.TIMEOUT_S)
            except:
                UploadLog.log(f"Failed to log telemetry")

    def hasLicense(self, capability, licenses):
        return capability.name in licenses

    def isUsed(self, capability):
        used = [cap.name for cap in self.options.capabilities]
        return capability.name in used
