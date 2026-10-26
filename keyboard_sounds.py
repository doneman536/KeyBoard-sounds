#!/usr/bin/env python3
"""
Keyboard Sounds Daemon for macOS (Apple Silicon / Intel)
Plays custom sounds on specific key presses with throttling.

Triggers:
- Delete / Backspace: faaah.mp3
- Esc: among-us-role-reveal-sound.mp3
- Caps Lock: cat-laugh-meme-1.mp3
- Shift: shocked-sound-effect.mp3
- Space: shot-gun.mp3

Throttle: 1.0s per sound trigger.
"""

import sys
import os
import time
import logging
import threading
import subprocess
from pathlib import Path
from pynput import keyboard
from pynput.keyboard import Key

# Setup paths
SCRIPT_DIR = Path(__file__).resolve().parent
SOUNDS_DIR = SCRIPT_DIR / "sounds"
LOG_DIR = Path.home() / "Library" / "Logs" / "KeyboardSounds"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "daemon.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

# Sound file mappings
SOUND_MAP = {
    "delete": SOUNDS_DIR / "faaah.mp3",
    "esc": SOUNDS_DIR / "among-us-role-reveal-sound.mp3",
    "caps_lock": SOUNDS_DIR / "cat-laugh-meme-1.mp3",
    "shift": SOUNDS_DIR / "shocked-sound-effect.mp3",
    "space": SOUNDS_DIR / "shot-gun.mp3",
}

# Verify sound files exist
for name, path in SOUND_MAP.items():
    if not path.is_file():
        logging.warning(f"Sound file not found for '{name}': {path}")
    else:
        logging.info(f"Loaded sound for '{name}': {path.name}")

# Throttling dictionary: 1.0 second throttle per trigger
THROTTLE_SECONDS = 2.0
last_trigger_times = {}
throttle_lock = threading.Lock()


def play_sound(sound_key: str, sound_path: Path):
    """
    Plays a sound using macOS native afplay asynchronously.
    Enforces a 1.0s throttle per sound.
    """
    now = time.time()
    with throttle_lock:
        last_time = last_trigger_times.get(sound_key, 0.0)
        if now - last_time < THROTTLE_SECONDS:
            return
        last_trigger_times[sound_key] = now

    if not sound_path.is_file():
        logging.error(f"Cannot play sound, file missing: {sound_path}")
        return

    try:
        logging.info(f"Triggered sound: {sound_key} ({sound_path.name})")
        subprocess.Popen(
            ["/usr/bin/afplay", str(sound_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as err:
        logging.error(f"Failed to execute afplay for {sound_key}: {err}")


def is_shift_key(key) -> bool:
    return key in (Key.shift, Key.shift_l, Key.shift_r) or getattr(key, 'vk', None) in (56, 60)


def on_press(key):
    # 1. Escape
    if key == Key.esc:
        play_sound("esc", SOUND_MAP["esc"])
        return

    # 2. Delete / Backspace
    if key in (Key.backspace, Key.delete):
        play_sound("delete", SOUND_MAP["delete"])
        return

    # 3. Caps Lock
    if key == Key.caps_lock:
        play_sound("caps_lock", SOUND_MAP["caps_lock"])
        return

    # 4. Space
    if key == Key.space:
        play_sound("space", SOUND_MAP["space"])
        return

    # 5. Shift
    if is_shift_key(key):
        play_sound("shift", SOUND_MAP["shift"])
        return


def main():
    logging.info("Keyboard Sounds Daemon starting...")
    logging.info(f"Project directory: {SCRIPT_DIR}")
    logging.info(f"Sounds directory: {SOUNDS_DIR}")
    logging.info(f"Throttle duration: {THROTTLE_SECONDS}s")
    logging.info(f"Logs: {LOG_FILE}")

    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        logging.info("Keyboard Sounds Daemon stopped by user.")
    except Exception as e:
        logging.critical(f"Listener error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
