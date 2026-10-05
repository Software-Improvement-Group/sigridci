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

function toggleRowVisibility(technologySupportTable, categoryIndex, withoutText, inverse=false) {
    for (const row of technologySupportTable.querySelectorAll("tr")) {
        let unavailable = withoutText && row.innerText.indexOf(withoutText) !== -1;
        if (inverse) {
            unavailable = !unavailable;
        }
        row.querySelectorAll("td").forEach(td => td.classList.toggle("unavailable", unavailable));
    }

    const technologySupportLinks = document.querySelectorAll(".technologySupportCategories a");
    technologySupportLinks.forEach((link, i) => link.classList.toggle("active", i === categoryIndex));

    return false;
}

document.addEventListener("DOMContentLoaded", () => {
    const technologySupportLinks = document.querySelectorAll(".technologySupportCategories a");
    const table = document.querySelector(".technologySupportTable");

    if (table) {
        if (technologySupportLinks.length >= 4) {
            technologySupportLinks[0].addEventListener("click", e => toggleRowVisibility(table, 0, ""));
            technologySupportLinks[1].addEventListener("click", e => toggleRowVisibility(table, 1, "(1)"));
            technologySupportLinks[2].addEventListener("click", e => toggleRowVisibility(table, 2, "(4)"));
            technologySupportLinks[3].addEventListener("click", e => toggleRowVisibility(table, 3, "Guardrails", true));
        }

        toggleRowVisibility(table, 0, "");
    }
});
