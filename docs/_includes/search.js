{%- assign index = "" | split: "" -%}

{%- for page in site.html_pages -%}
    {%- assign index = index | push: page | uniq -%}
{%- endfor -%}

const searchIndex = {};

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

function fillSearchIndex(item) {
    searchIndex[item.title] = item;
}

{%- for document in index -%}
    fillSearchIndex({
        title: {{ document.title | smartify | strip_html | normalize_whitespace | jsonify }},
        content: {{ document.content | strip_html | normalize_whitespace | jsonify }},
        url: "{{ document.url }}"
    });
{%- endfor -%}

function filterSearchResults(entry, input) {
    const item = searchIndex[entry.label];
    const titleMatch = item.title.toLowerCase().indexOf(input.toLowerCase()) != -1;
    const contentMatch = item.content.toLowerCase().indexOf(input.toLowerCase()) != -1;
    return titleMatch || contentMatch;
}

function styleSearchResult(entry, input) {
    const listItem = document.createElement("li");
    listItem.innerText = searchIndex[entry.label].title;
    return listItem;
}

document.addEventListener("DOMContentLoaded", () => {
    const searchBox = document.getElementById("searchQuery");

    new Awesomplete(searchBox, {
        list: Object.keys(searchIndex),
        filter: filterSearchResults,
        item: styleSearchResult
    });
    
    searchBox.addEventListener("awesomplete-select", e => document.location.href = searchIndex[e.text.label].url);
});
