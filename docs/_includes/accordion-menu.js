function expandCurrentSection() {
    const categoryHeaders = document.querySelectorAll("nav .category");
    const categoryPages = document.querySelectorAll("nav .pages");

    for (let i = categoryHeaders.length - 1; i >= 0; i--) {
    console.log(i);
        console.log(categoryHeaders[i]);
        console.log(categoryPages[i]);
        const currentPageLink = findCurrentPageLink(categoryPages[i]);

        if (currentPageLink) {
            console.log(currentPageLink);
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
    
    for (let i = 0; i < categoryHeaders.length; i++) {
        categoryHeaders[i].addEventListener("click", e => expandSection(i));
    }
});
