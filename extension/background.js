// background.js
const t = chrome.i18n.getMessage;

// Item in context menu
chrome.runtime.onInstalled.addListener(() => {
    console.log("background.js: " + t("script_installed"));

    chrome.contextMenus.create({
        id: "openInExternalPlayer",
        title: t("open_in_player"),
        contexts: ["page", "link"]
    });
});

// Listener for context menu
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "openInExternalPlayer") {
        const url = info.linkUrl || info.pageUrl;
        console.log("background.js: URL:", url);

        if (url) {
            if (url && (url.includes("youtube.com/watch?v=") || url.includes("youtu.be/"))) {
                console.log("baground.js: " + t("trying_python_script"), url);
                sendMessageToPython(url);
            } else {
                console.warn("background.js: " + t("not_youtube"), url);
            }
        }
    }
});

// Sends msg to Python
function sendMessageToPython(videoUrl) {
    console.log("background.js: " + t("sending_to_python"), videoUrl);

    const hostName = "com.yt.h264";

    chrome.runtime.sendNativeMessage(
        hostName,
        { text: videoUrl },
        (response) => {
            if (chrome.runtime.lastError) {
                console.error("background.js: " + t("error_native_msg"), chrome.runtime.lastError.message);
            } else {
                console.log("background.js: " + t("python_reponse"), response);
            }
        }
    );
}
