// Copyright Software Improvement Group
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

document.addEventListener("DOMContentLoaded", () => {
    const _paq = window._paq = window._paq || [];
    _paq.push(["trackPageView"]);
    _paq.push(["enableLinkTracking"]);
    _paq.push(["setCustomUrl", document.location.href]);
    _paq.push(["setTrackerUrl", "https://sigrid-says.com/usage/matomo.php"]);
    _paq.push(["setSiteId", "4"]);

    const statsElement = document.createElement("script");
    statsElement.async = true;
    statsElement.src = "https://sigrid-says.com/usage/matomo.js";
    document.head.appendChild(statsElement);
});
