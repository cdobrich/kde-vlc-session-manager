#!/bin/bash
### BEGIN INIT INFO
# Provides:          kde-vlc-session-manager
# Required-Start:    $local_fs
# Required-Stop:     $local_fs
# Default-Start:     S
# Default-Stop:      1
# Short-Description: Save and reopen opened VLC videos between sessions.
# Description: Save and reopen opened VLC videos between sessions.
#
# Place this script into /etc/init.d/ and make a symlink in whatever Runlevel folder as desired. Typically:
#
#		ln -s /etc/init.d/kde-vlc-session-manager.sh  /etc/rc5/s90kde-vlc-session-manager.sh
#
### END INIT INFO

set -e

case "$1" in
	start)
    ;;
  status)
		;;
	*)
    echo "Usage: /etc/init.d/kde-vlc-session-manager.sh {start|status}"
    exit 1
    ;;
esac

exit 0
