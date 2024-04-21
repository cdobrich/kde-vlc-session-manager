# kde-vlc-session-manager

(WIP Documentation)

A program combined with a system-script to save the videos are currently open with the program VLC and then will reopen those videos upon reboot (also known as session resume)

The stored session information will contain a file to the currently open media AND the position (time) it was at when saved.

## Information Not Currently Stored

Loop status
Loop marks

# How to Use

## Command to save current videos
```
kde-vlc-session-manager.py save
```

## Command to restore videos
```
kde-vlc-session-manager.py restore
```

## Required Python Packages

### Requests

See also the _requirements.txt_ file:

`pip install dbus-python`

# Session Storage Information & Location

Video session information is stored in the user's home directory.

```$USER/.vlc_session```

    
