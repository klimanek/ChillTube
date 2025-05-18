# ChillTube

**Lightweight Chrome extension that offloads YouTube video playback to MPV player using hardware-accelerated H.264.**  
Ideal for older laptops where VP9/AV1 decoding is not hardware-accelerated.

---

## 🔧 Why use this?

Modern YouTube videos use VP9 or AV1, which often lack hardware acceleration on older systems. This leads to:
- 🔥 High CPU usage  
- 🌪 Loud fans  
- 🔋 Reduced battery life  

This extension:
- 🧊 Keeps your laptop cooler  
- 🔇 Runs quieter  
- 🔋 Improves battery life  
- 🎞 Uses MPV with H.264 fallback (hardware-accelerated)

---

## ✅ Features

- Adds a toolbar button and right-click menu
- Sends current YouTube video URL to native Python script
- Plays video in MPV with a format string that prefers H.264
- Works out-of-the-box on **Linux**

---

## ⚠️ System Requirements

- ✅ **Supported:** Linux (x11/Wayland)
- ❌ macOS: not yet supported (due to app sandbox and MPV launch issues)
- ❌ Windows: not yet supported

---

## 🛠️ Installation

### 1a. Download the zip archive
from here and extract it locally, or...

### 1b. Clone this repo
```bash
git clone https://github.com/klimanek/ChillTube
```

### 2. Load the extension in your browser
- Go to `chrome://extensions/` 
- Enable Developer Mode
- Click Load unpacked and select the `extension` folder
- Copy the extension ID

### 3. Install native messaging host
```bash
cd ChillTube
```


```bash
# ChillTube package structure
├── install.sh
├── README.md
├── extension
└── yt_h264.py
```


Open `install.sh` in your favorite text editor and insert the copied extension ID:

```bash
EXT_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # change that
```

Then run:

```bash
sh install.sh
```


## 🌍 Localization
Currently supported:

- 🇬🇧 English
- 🇨🇿 Czech

Feel free to contribute translations in your language!


## 📌 Roadmap
- Add macOS support (via IINA?)
- Optional in-video button
- Preferences/config panel
- Windows support

## 📜 License
MIT

## 🔍 Related keywords
YouTube overheat, loud fans, battery drain, MPV player, H.264 fallback, yt-dlp helper, external player for YouTube, Chromium extension, older laptops, fanless playback, AV1 problem, VP9 decoding issues

<!--
Keywords: YouTube overheating, fan noise, battery drain, watch YouTube in MPV, yt-dlp extension, play YouTube in external player, hardware accelerated YouTube, slow YouTube playback, reduce CPU usage YouTube, VP9 issue, AV1 lag, quiet laptop YouTube
-->
