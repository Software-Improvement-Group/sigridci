function expandCurrentSection() {
    const sections = document.querySelectorAll(".toc input[type=checkbox]");
    const panels = document.querySelectorAll(".toc .pages");

    for (let i = 0; i < sections.length; i++) {
        const currentPageLink = findCurrentPageLink(panels[i]);
        
        if (currentPageLink) {
            sections[i].checked = true;
            currentPageLink.classList.add("currentSection");
            return;
        }
    }          
}

function findCurrentPageLink(panel) {
    const links = [...panel.querySelectorAll("a.page")];
    return links.find(link => document.location.pathname.startsWith(link.getAttribute("href")));
}

document.addEventListener("DOMContentLoaded", event => expandCurrentSection());
