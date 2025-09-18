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

function expandCurrentSection() {
    const categoryHeaders = document.querySelectorAll("nav .category");
    const categoryPages = document.querySelectorAll("nav .pages");

    for (let i = categoryHeaders.length - 1; i >= 0; i--) {
        const currentPageLink = findCurrentPageLink(categoryPages[i]);

        if (currentPageLink) {
            expandSection(i);
            currentPageLink.classList.add("currentPage");
            return;
        }
    }
}

function expandSection(index) {
    const categoryHeaders = document.querySelectorAll("nav .category");
    const categoryPages = document.querySelectorAll("nav .pages");
    
    if (categoryHeaders[index].classList.contains("currentCategoryHeader")) {
        categoryHeaders[index].classList.remove("currentCategoryHeader");
        categoryPages[index].classList.remove("currentCategory");
    } else {
        categoryHeaders[index].classList.add("currentCategoryHeader");
        categoryPages[index].classList.add("currentCategory");
    }
}

function findCurrentPageLink(panel) {
    const links = [...panel.querySelectorAll("a.page")];
    links.reverse();
    return links.find(link => document.location.pathname.startsWith(link.getAttribute("href")));
}

document.addEventListener("DOMContentLoaded", () => {
    expandCurrentSection();
    
    const categoryHeaders = document.querySelectorAll("nav .category");
    const hamburger = document.querySelector(".hamburger");
    
    for (let i = 0; i < categoryHeaders.length; i++) {
        categoryHeaders[i].addEventListener("click", e => expandSection(i));
    }

    hamburger.addEventListener("click", e => {
        const menu = document.querySelector("nav");
        console.log(menu.style.display);
        menu.style.display = menu.style.display == "block" ? "none" : "block";
    });
});
