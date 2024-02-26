#!/usr/bin/env bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title New Private Window
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🕶️

# Documentation:
# @raycast.description Open a new Safari private window.
# @raycast.author mohdfareed
# @raycast.authorURL https://raycast.com/mohdfareed

#!/usr/bin/env zsh

osascript -e 'tell application "Safari"
    activate
    tell application "System Events"
        keystroke "n" using {command down, shift down}
    end tell
end tell'
