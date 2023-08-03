document.addEventListener("DOMContentLoaded", () => {
    const url = document.location.href;
    const t = new Date().getTime();

    const stats = document.createElement("img");
    stats.addEventListener("load", e => stats.style.display = "none");
    stats.src = "https://sigrid-says.com/usage/matomo.php?idsite=4&amp;rec=1&amp;url=" + url + "&amp;t=" + t;
    document.querySelector("body").appendChild(stats);
});
