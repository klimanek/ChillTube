#!/bin/bash

# Config
EXT_ID="egloiofgpokfincpignmkaikpkdnbnpk"  # use a real ID (see extensions in Chrome)

SCRIPT_PATH="$HOME/.local/bin/yt_h264.py"

# if [[ "$OSTYPE" == "darwin"* ]]; then
#     MANIFEST_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
#     echo "Platform: macOS"
if [[ "$OSTYPE" == "linux"* ]]; then
    MANIFEST_DIR="$HOME/.config/google-chrome/NativeMessagingHosts"
    echo "Platform: Linux"
elif [[ "$OSTYPE" == "freebsd"* ]]; then
    MANIFEST_DIR="$HOME/.config/google-chrome/NativeMessagingHosts"
    echo "Platform: FreeBSD"
else
    echo "Unsupported OS."
    exit 1
fi

MANIFEST_PATH="$MANIFEST_DIR/com.yt.h264.json"

# Create directories
mkdir -p "$(dirname "$SCRIPT_PATH")"
mkdir -p "$MANIFEST_DIR"

# Copy the py script
cp yt_h264.py "$SCRIPT_PATH"
chmod +x "$SCRIPT_PATH"

# Manifest
cat > "$MANIFEST_PATH" <<EOF
{
    "name": "com.yt.h264",
    "description": "YT → External Player bridge",
    "path": "$SCRIPT_PATH",
    "type": "stdio",
    "allowed_origins": [
    "chrome-extension://$EXT_ID/"
    ]
}
EOF

echo "Everything's fine."

