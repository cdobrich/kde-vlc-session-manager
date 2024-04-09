#!/usr/bin/env python3

import os
import subprocess
import traceback

import dbus

# Define the path to store session information
SESSION_FILE = os.path.expanduser("~/.vlc_session")


# Function to save session information
def save_session():
    vlc_instances = subprocess.check_output(["pgrep", "vlc"]).decode().split()
    with open(SESSION_FILE, "w") as session_file:
        for pid in vlc_instances:
            session_file.write(get_video_info(pid))


def get_video_info(pid):
    session_info = ""
    bus = dbus.SessionBus()
    try:
        player_obj = bus.get_object("org.mpris.MediaPlayer2.vlc", f"/org/mpris/MediaPlayer2")
        # player_obj = bus.get_object("org.mpris.MediaPlayer2.vlc", f"/org/mpris/MediaPlayer2/vlc{pid}")
        player_iface = dbus.Interface(player_obj, "org.freedesktop.DBus.Properties")
        metadata = player_iface.Get("org.mpris.MediaPlayer2.Player", "Metadata")
        if metadata:
            location = metadata["xesam:url"]
            position = player_iface.Get("org.mpris.MediaPlayer2.Player", "Position")
            session_info += f"{location} {position}\n"
        return session_info
    except dbus.exceptions.DBusException as e:
        print(f"Error: {e}")
        traceback.print_exception(type(e))
        return None


# Function to restore session
def restore_session():
    if not os.path.exists(SESSION_FILE):
        return
    with open(SESSION_FILE, "r") as session_file:
        for line in session_file:
            video, position = line.strip().split()
            subprocess.Popen(["vlc", video, f"--start-time={position}"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Save and restore VLC session.")
    parser.add_argument("action", choices=["save", "restore"], help="Action to perform (save or restore)")
    args = parser.parse_args()

    if args.action == "save":
        save_session()
    elif args.action == "restore":
        restore_session()
