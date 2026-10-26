#!/usr/bin/env bash
set -e

PLIST_NAME="com.user.keyboardsounds.plist"
SOURCE_PLIST="$(cd "$(dirname "$0")" && pwd)/${PLIST_NAME}"
TARGET_DIR="${HOME}/Library/LaunchAgents"
TARGET_PLIST="${TARGET_DIR}/${PLIST_NAME}"
LOG_DIR="${HOME}/Library/Logs/KeyboardSounds"

echo "=== Installing Keyboard Sounds Daemon ==="

# 1. Create target directories if they don't exist
mkdir -p "${TARGET_DIR}"
mkdir -p "${LOG_DIR}"

# 2. Unload existing service if currently loaded
if launchctl list | grep -q "com.user.keyboardsounds"; then
    echo "Unloading existing keyboard sounds daemon..."
    launchctl unload "${TARGET_PLIST}" 2>/dev/null || true
fi

# 3. Ensure plist exists (generate from .example if missing)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ ! -f "${SOURCE_PLIST}" ] && [ -f "${SOURCE_PLIST}.example" ]; then
    echo "Generating ${PLIST_NAME} from template..."
    sed -e "s|/PATH/TO/PROJECT|${PROJECT_DIR}|g" \
        -e "s|YOUR_USERNAME|${USER}|g" \
        "${SOURCE_PLIST}.example" > "${SOURCE_PLIST}"
fi

# 4. Copy plist into ~/Library/LaunchAgents/
echo "Copying ${PLIST_NAME} to ${TARGET_DIR}..."
cp "${SOURCE_PLIST}" "${TARGET_PLIST}"

# 4. Load the service into launchd
echo "Loading daemon with launchctl..."
launchctl load "${TARGET_PLIST}"

# 5. Verify status
sleep 1
if launchctl list | grep -q "com.user.keyboardsounds"; then
    echo "✓ Daemon installed and running successfully!"
    echo "  Status:"
    launchctl list | grep "com.user.keyboardsounds"
    echo ""
    echo "Logs are located at:"
    echo "  ${LOG_DIR}/daemon.log"
    echo "  ${LOG_DIR}/stdout.log"
    echo "  ${LOG_DIR}/stderr.log"
    echo ""
    echo "NOTE: On macOS, listening to global keystrokes requires Accessibility permissions."
    echo "If sounds do not trigger, add Python to Accessibility clients in:"
    echo "System Settings -> Privacy & Security -> Accessibility"
    echo ""
    echo "You can quickly open this setting by running:"
    echo "  open 'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'"
    echo "And ensure '/Users/kaif/Desktop/Projects/KeyBoard-sounds/.venv/bin/python3' (or your Terminal) is enabled."
else
    echo "⚠️ Daemon loaded, but might have encountered an issue. Check logs:"
    echo "cat ${LOG_DIR}/stderr.log"
fi
