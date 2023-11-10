{%- assign index = "" | split: "" -%}

{%- for page in site.html_pages -%}
    {%- assign index = index | push: page | uniq -%}
{%- endfor -%}

const searchIndex = {};

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
