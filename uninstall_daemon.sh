#!/usr/bin/env bash
set -e

PLIST_NAME="com.user.keyboardsounds.plist"
TARGET_PLIST="${HOME}/Library/LaunchAgents/${PLIST_NAME}"

echo "=== Uninstalling Keyboard Sounds Daemon ==="

if [ -f "${TARGET_PLIST}" ]; then
    echo "Unloading daemon from launchctl..."
    launchctl unload "${TARGET_PLIST}" 2>/dev/null || true
    echo "Removing plist from ~/Library/LaunchAgents/..."
    rm -f "${TARGET_PLIST}"
    echo "✓ Daemon unloaded and removed."
else
    echo "Plist file not found at ${TARGET_PLIST}. Checking running process..."
    launchctl remove com.user.keyboardsounds 2>/dev/null || true
fi

echo "Stopped keyboard sounds service."
