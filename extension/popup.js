document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("launch");
    const status = document.getElementById("status");
    const checkbox = document.getElementById('autoplayCheckbox');

    const t = chrome.i18n.getMessage;

    button.textContent = t("open_external");

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const tab = tabs[0];

        if (!tab || !tab.url || !tab.url.includes("youtube.com/watch")) {
            status.textContent = t("not_youtube");
            button.disabled = true;
            return;
        }

        // AUTOPLAY
        // Read the value of the checkboxu (autoplay)
        chrome.storage.local.get('yt_mpv_autoplay', (data) => {
            if (typeof data.yt_mpv_autoplay === 'boolean') {
                checkbox.checked = data.yt_mpv_autoplay;
            } else {
                // První spuštění – nastavíme výchozí hodnotu (false)
                chrome.storage.local.set({ yt_mpv_autoplay: false });
                checkbox.checked = false;
            }
        });

        // Uložení nového stavu při změně checkboxu
        checkbox.addEventListener('change', () => {
            chrome.storage.local.set({ yt_mpv_autoplay: checkbox.checked });
        });

        // External player launch
        button.addEventListener("click", () => {
            button.disabled = true;
            status.innerHTML = `<span class="spinner"></span>${t("opening")}`;

            const message = { text: tab.url };

            chrome.runtime.sendNativeMessage("com.yt.h264", message, (response) => {
                if (chrome.runtime.lastError) {
                    console.error(chrome.runtime.lastError.message);
                    status.textContent = t("error");
                } else {
                    setTimeout(() => {
                        status.textContent = t("done");
                        setTimeout(() => window.close(), 2000);
                    }, 4300);
                }

            });
        });
    });
});
