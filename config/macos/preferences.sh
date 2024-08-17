# General
# =======

# set computer name and local host name
scutil --set ComputerName "Mohd's MacBook"
scutil --set LocalHostName "mohds-macbook"
# reduce wallpaper tinting in windows
defaults write .GlobalPreferences AppleReduceDesktopTinting -bool true
# rearrange spaces based on most recent use
defaults write com.apple.dock mru-spaces -bool false
# autohide dock
defaults write com.apple.dock autohide -bool true
# show the ~/Library folder
chflags nohidden ~/Library && xattr -d com.apple.FinderInfo ~/Library > /dev/null 2>&1

# trackpad, mouse, and keyboard
# =============================

# key repeat
defaults write .GlobalPreferences KeyRepeat -int 2
# delay until key repeat
defaults write .GlobalPreferences InitialKeyRepeat -int 25
# trackpad dragging
defaults write com.apple.AppleMultitouchTrackpad Dragging -int 1
defaults write com.apple.AppleMultitouchTrackpad DragLock -int 1
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Dragging -int 1
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad DragLock -int 1
