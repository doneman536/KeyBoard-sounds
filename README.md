# Keyboard Sounds Daemon for macOS

A lightweight, non-blocking background daemon for macOS (optimized for Apple Silicon M1/M2/M3 and Intel) that triggers sound effects on specific key presses and keyboard shortcuts with throttling to prevent unwanted duplicate sounds.

---

## 🎵 Sound Triggers & Mappings

| Key / Shortcut | Sound Effect | File | Behavior |
| :--- | :--- | :--- | :--- |
| **Delete / Backspace** | Faaah | `sounds/faaah.mp3` | Throttled (0.5s) |
| **Esc** | Among Us Role Reveal | `sounds/among-us-role-reveal-sound.mp3` | Throttled (0.5s) |
| **Caps Lock** | Cat Laugh Meme | `sounds/cat-laugh-meme-1.mp3` | Throttled (0.5s) |
| **Shift** | Shocked Sound Effect | `sounds/shocked-sound-effect.mp3` | Throttled (0.5s, suppressed when Cmd is held) |
| **Cmd + Shift + 3 or 4** | Camera Shutter (Zvuk) | `sounds/zvuk-fotoapparata.mp3` | **2-second delay**, Throttled (0.5s) |
| **Space** | Shotgun | `sounds/shot-gun.mp3` | Throttled (0.5s) |

---

## ⚙️ How It Works

- **Engine:** Built with Python `pynput` listener hooking into macOS CoreGraphics event stream.
- **Audio Playback:** Uses macOS built-in `/usr/bin/afplay` in non-blocking background processes (zero external audio libraries needed).
- **Throttling:** 0.5s per sound trigger prevents repeated or rapid multi-triggers.
- **macOS LaunchAgent:** Installed as a persistent user service (`~/Library/LaunchAgents/com.user.keyboardsounds.plist`) with `KeepAlive` and `RunAtLoad` enabled so it automatically runs in the background and starts on boot/login.

---

## 🚀 Quick Setup & Installation

### 1. Install & Start as Background Daemon
In the project directory, run:
```bash
./install_daemon.sh
```
This will:
- Copy the configuration to `~/Library/LaunchAgents/com.user.keyboardsounds.plist`
- Start the service immediately via `launchctl`
- Keep it running even after Mac restarts

### 2. Grant macOS Accessibility Permission (Required on macOS)
macOS requires Accessibility permissions for applications or scripts that monitor global keystrokes:
1. Open **System Settings** -> **Privacy & Security** -> **Accessibility**.
2. Ensure your terminal app (e.g. **Terminal**, **iTerm2**, or **Python**) is toggled **ON**.

---

## 🧪 Testing in Foreground (Interactive Test)

You can also run the script directly in your terminal to test keys and hear audio in real time:
```bash
./.venv/bin/python3 keyboard_sounds.py
```
Press `Ctrl + C` to stop.

---

## 📋 Monitoring & Logs

Log files are kept in `~/Library/Logs/KeyboardSounds/`:
- **Real-time activity log:**
  ```bash
  tail -f ~/Library/Logs/KeyboardSounds/daemon.log
  ```
- **Error log:**
  ```bash
  cat ~/Library/Logs/KeyboardSounds/stderr.log
  ```

---

## 🛑 Stopping & Uninstalling

To stop and remove the daemon from starting on boot:
```bash
./uninstall_daemon.sh
```
