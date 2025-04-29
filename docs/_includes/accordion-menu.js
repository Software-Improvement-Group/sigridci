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
