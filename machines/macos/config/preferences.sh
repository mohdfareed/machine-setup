# set local host name
scutil --set LocalHostName "mohds-macbook"
# keyboard repeat rate
defaults write NSGlobalDomain KeyRepeat -int 2
# keyboard repeat delay
defaults write NSGlobalDomain InitialKeyRepeat -int 15
# keyboard navigation
defaults write NSGlobalDomain AppleKeyboardUIMode -int 2
# tap to click
defaults write com.apple.AppleMultitouchTrackpad Clicking -bool true
# drag with trackpad
defaults write com.apple.AppleMultitouchTrackpad Dragging -bool true

# reduce wallpaper tinting in windows
defaults write .GlobalPreferences AppleReduceDesktopTinting -bool true
# rearrange spaces based on most recent use
defaults write com.apple.dock mru-spaces -bool false
# switch windows in same space
defaults write NSGlobalDomain AppleSpacesSwitchOnActivate -bool false
# enable app expose
defaults write com.apple.dock showAppExposeGestureEnabled -bool true

# auto-hide dock
defaults write com.apple.dock autohide -bool true
# hide recent apps
defaults write com.apple.dock show-recents -bool false
# minimize with scaling
defaults write com.apple.dock mineffect -string "scale"
