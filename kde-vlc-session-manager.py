#!/usr/bin/env python3

import os
import subprocess
import traceback

import dbus

# Define the path to store session information
SESSION_FILE = os.path.expanduser("~/.vlc_session")


# Function to save session information
def save_session():
    """
    When polling the Linux DBUS, it is necessary to search for the program
    name WITHOUT a 'pid' and then for any other processes using the name using
    'program_name.instance{pid}'. These results must be combined.
    """
    vlc_instances = subprocess.check_output(["pgrep", "vlc"]).decode().split()
    if not vlc_instances:
        print("No VLC instances found.")
        return

    with open(SESSION_FILE, "w") as session_file:
        video_list = []
        for pid in vlc_instances:
            video_info = get_video_info(pid)
            if video_info:
                video_list.append(video_info)

        video_info = get_vide_info_no_pid()
        if video_info:
            video_list.append(video_info)

        for item in video_list:
            session_file.write(item)


def get_vide_info_no_pid():
    session_info = ""
    bus = dbus.SessionBus()
    try:
        player_obj1 = bus.get_object("org.mpris.MediaPlayer2.vlc", f"/org/mpris/MediaPlayer2")
        player_iface1 = dbus.Interface(player_obj1, "org.freedesktop.DBus.Properties")
        metadata1 = player_iface1.Get("org.mpris.MediaPlayer2.Player", "Metadata")
        if metadata1:
            location = metadata1["xesam:url"]
            position = player_iface1.Get("org.mpris.MediaPlayer2.Player", "Position")
            session_info += f"{location} {position}\n"
        return session_info
    except dbus.exceptions.DBusException as e:
        print(f"Error: {e}")
        return None


def get_video_info(pid):
    session_info = ""
    bus = dbus.SessionBus()
    try:
        player_obj2 = bus.get_object("org.mpris.MediaPlayer2.vlc.instance" + str(pid), f"/org/mpris/MediaPlayer2")
        player_iface2 = dbus.Interface(player_obj2, "org.freedesktop.DBus.Properties")
        metadata2 = player_iface2.Get("org.mpris.MediaPlayer2.Player", "Metadata")
        if metadata2:
            location = metadata2["xesam:url"]
            position = player_iface2.Get("org.mpris.MediaPlayer2.Player", "Position")
            session_info += f"{location} {position}\n"
        return session_info

    except dbus.exceptions.DBusException as e:
        print(f"Error: {e}")
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
