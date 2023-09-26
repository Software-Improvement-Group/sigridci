document.addEventListener("DOMContentLoaded", () => {
    const _paq = window._paq = window._paq || [];
    _paq.push(["trackPageView"]);
    _paq.push(["enableLinkTracking"]);
    _paq.push(["setCustomUrl", document.location.href]);
    _paq.push(["setTrackerUrl", "https://sigrid-says.com/usage/matomo.php"]);
    _paq.push(["setSiteId", "4"]);

    const statsElement = document.createElement("script");
    statsElement.async = true;
    statsElement.src = "https://sigrid-says.com/usage/matomo.js";
    document.head.appendChild(statsElement);
});
