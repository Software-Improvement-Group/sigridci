window.wxOConfiguration = {
    orchestrationID: "20260107-1057-3552-4092-a780179eecda_20260120-0849-3953-301e-4304a7ed33aa",
    hostURL: "https://eu-central-1.dl.watson-orchestrate.ibm.com",
    rootElementID: "root",
    chatOptions: {
        agentId: "d0cdc744-ca5d-4d6e-8dfe-2ca0f8cd77ab",
        agentEnvironmentId: "b49d8d53-0c85-426a-8a66-6649452ebbdc",
        isPublic: true,
    }
};
setTimeout(function () {
    const script = document.createElement('script');
    script.src = `${window.wxOConfiguration.hostURL}/wxochat/wxoLoader.js?embed=true`;
    script.addEventListener('load', function () {
        wxoLoader.init();
    });
    document.head.appendChild(script);
}, 0);
