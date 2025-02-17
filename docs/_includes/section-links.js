function makeSectionLink(sectionHeader) {
    const sectionLink = document.createElement("div");
    sectionLink.classList.add("sectionLink");
    sectionLink.title = "Copy a deep-link to this section to your clipboard.";
    sectionHeader.appendChild(sectionLink);

    sectionLink.addEventListener("click", e => {
        const url = getSectionHeaderURL(sectionHeader);
        navigator.clipboard.writeText(url);
        window.location.href = url;
    });
}

function getSectionHeaderURL(sectionHeader) {
    const anchor = sectionHeader.innerText.replace(/\s/g, "-").replace(/[^\w-]/g, "").toLowerCase();
    return window.location.origin + window.location.pathname + "#" + anchor;
}

function makeTableOfContents(toc, sectionHeaders) {
    const title = document.createElement("h4");
    title.innerText = "On this page";
    toc.appendChild(title);

    const list = document.createElement("ul");
    toc.appendChild(list);
    
    for (const sectionHeader of sectionHeaders) {
        if (sectionHeader.nodeName != "h1") {
            const listItem = document.createElement("li");
            listItem.classList.add(sectionHeader.nodeName.toLowerCase());
            list.appendChild(listItem);
        
            const sectionLink = document.createElement("a");
            sectionLink.innerText = sectionHeader.innerText;
            sectionLink.href = getSectionHeaderURL(sectionHeader);
            listItem.appendChild(sectionLink);
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const sectionHeaders = document.querySelectorAll("article h2, article h3, article h4");
    const toc = document.querySelector("sig-toc");

    for (const sectionHeader of sectionHeaders) {
        makeSectionLink(sectionHeader);
    }
    
    if (toc && sectionHeaders.length > 0) {
        makeTableOfContents(toc, sectionHeaders);
    }
});
