{%- assign index = "" | split: "" -%}

{%- for page in site.html_pages -%}
    {%- assign index = index | push: page | uniq -%}
{%- endfor -%}

const searchIndex = {};

{%- for document in index -%}
    searchIndex[{{ document.title | smartify | strip_html | normalize_whitespace | jsonify }}] = {{ document.content | strip_html | normalize_whitespace | jsonify }};
{%- endfor -%}

/*const lunrSearch = lunr(function () {
    this.ref("name");
    this.field("text");

    searchIndex.forEach(function (doc) {
        this.add(doc)
    }, this)
});*/

document.addEventListener("DOMContentLoaded", () => {
    new Awesomplete(document.getElementById("searchResults"), {
        list: Object.keys(searchIndex),
        filter: (item, input) => {
            console.log("filter");
            console.log(item);
            return item.toLowerCase().indexOf(input.toLowerCase()) != -1;
        }
    });
});
