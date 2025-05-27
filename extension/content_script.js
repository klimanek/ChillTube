// Trying to pause the video
function tryPauseVideo(retries = 20) {
    const video = document.querySelector('video');
    if (video && !video.paused) {
        video.pause();
        console.log("[yt-mpv] Paused autoplay video");
    } else if (retries > 0) {
        setTimeout(() => tryPauseVideo(retries - 1), 300);
    }
}

// Wachting SPA URL changes 
let lastUrl = location.href;
new MutationObserver(() => {
    if (location.href !== lastUrl) {
        lastUrl = location.href;
        setTimeout(() => tryPauseVideo(), 500); // just wait a bit
    }
}).observe(document, { subtree: true, childList: true });

// Play it at first load
tryPauseVideo();

// Autoplay
chrome.storage.local.get(['yt_mpv_autoplay'], (result) => {
    if (!result.yt_mpv_autoplay) {
        tryPauseVideo();
    }
});
