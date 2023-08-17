# General
# =======

echo "Setting up general preferences..."
# set computer name and local host name
scutil --set ComputerName "Mohd's MacBook"
scutil --set LocalHostName "mohds-macbook"
# reduce wallpaper tinting in windows
defaults write .GlobalPreferences AppleReduceDesktopTinting -bool true
# rearrange spaces based on most recent use
defaults write com.apple.dock mru-spaces -bool false
# autohide dock
defaults write com.apple.dock autohide -bool true

# trackpad, mouse, and keyboard
# =============================

echo "Setting up trackpad, mouse, and keyboard preferences..."
# key repeat
defaults write .GlobalPreferences KeyRepeat -int 2
# delay until key repeat
defaults write .GlobalPreferences InitialKeyRepeat -int 25
# trackpad dragging
defaults write com.apple.AppleMultitouchTrackpad Dragging -int 1
defaults write com.apple.AppleMultitouchTrackpad DragLock -int 1
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Dragging -int 1
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad DragLock -int 1


# Finder
# ======

echo "Setting up Finder preferences..."
# when performing a search, use the current folder by default
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"
# keep folders on top when sorting by name
defaults write com.apple.finder _FXSortFoldersFirst -bool true
defaults write com.apple.finder _FXSortFoldersFirstOnDesktop -bool true
# show the ~/Library folder
chflags nohidden ~/Library && xattr -d com.apple.FinderInfo ~/Library > /dev/null 2>&1
# enable snap-to-grid for icons on the desktop and in other icon views
/usr/libexec/PlistBuddy -c "Set :DesktopViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist
/usr/libexec/PlistBuddy -c "Set :StandardViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist

# TextEdit
# ========

echo "Setting up TextEdit preferences..."
# use plain text mode for new TextEdit documents
defaults write com.apple.TextEdit RichText -int 0
# set windows dimensions
defaults write com.apple.TextEdit WidthInChars -int 80
defaults write com.apple.TextEdit HeightInChars -int 24
# plain text font
defaults write com.apple.TextEdit NSFixedPitchFont -string \
"JetBrainsMonoNerdFontComplete-Regular"
defaults write com.apple.TextEdit NSFixedPitchFontSize -int 14

# Terminal
# ========

# default Terminal profile
defaults write com.apple.Terminal "Default Window Settings" "Dark"
defaults write com.apple.Terminal "Startup Window Settings" "Dark"
# line marks
defaults write com.apple.Terminal ShowLineMarks -bool false
# secure keyboard entry
defaults write com.apple.terminal SecureKeyboardEntry -bool true
