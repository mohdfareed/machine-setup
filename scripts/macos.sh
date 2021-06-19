#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up macOS preferences...${clear}"

# check if dotfiles repo exists
if [[ ! -d $DOTFILES ]] ; then
    echo "${rbold}Error:${clear} DOTFILES directory does not exist..."
    return 1
fi

source $DOTFILES/dots/zshenv
# create link to personal music in Music folder
if [[ -d $iCloud/Music ]] ; then
	ln -siv $iCloud/Music $HOME/Music/Personal
fi
# close open System Preferences panes, to prevent them from overriding settings
osascript -e 'tell application "System Preferences" to quit'
# ask for the administrator password upfront
sudo -v

# General
# =======

# set computer name and local host name
scutil --set ComputerName "Mohd's MacBook"
scutil --set LocalHostName "Mohds-MacBook"
# reduce wallpaper tinting in windows
defaults write .GlobalPreferences AppleReduceDesktopTinting -bool true
# when switching to an application, switch to a space with open windows
defaults write .GlobalPreferences AppleSpacesSwitchOnActivate -bool false
# automatically rearrange spaces based on most recent use
defaults write com.apple.dock mru-spaces -bool false
# automatically hide and show the Dock
defaults write com.apple.dock autohide -bool true
# play feedback when volume is changed
defaults write .GlobalPreferences com.apple.sound.beep.feedback -bool true
# add wallpapers to preferences
defaults write com.apple.systempreferences DSKDesktopPrefPane "{
    UserFolderPaths =     (
        \"$DOTFILES/other/Wallpapers\"
    );
}"

# trackpad, mouse, and keyboard
# =============================

# tap to click
defaults write com.apple.AppleMultitouchTrackpad Clicking -bool true
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true
# double tap to drag items
defaults write com.apple.AppleMultitouchTrackpad Dragging -bool true
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Dragging -bool true
# mouse acceleration
defaults write .GlobalPreferences com.apple.mouse.scaling -int -1

# key repeat
defaults write .GlobalPreferences KeyRepeat -int 2
# delay until key repeat
defaults write .GlobalPreferences InitialKeyRepeat -int 25
# show input menu in menu bar
defaults write com.apple.TextInputMenu visible -bool true
# control strip customization
defaults write com.apple.controlstrip FullCustomized '(
    "com.apple.system.group.brightness",
    "com.apple.system.launchpad",
    "com.apple.system.group.keyboard-brightness",
    "com.apple.system.group.media",
    "com.apple.system.group.volume",
    "com.apple.system.workflows",
    "com.apple.system.screencapture"
)'
defaults write com.apple.controlstrip MiniCustomized '(
    "com.apple.system.group.brightness",
    "com.apple.system.group.volume",
    "com.apple.system.mute",
    "com.apple.system.screencapture"
)'

# Extensions
# ==========

# add workflows
ln -siv "$DOTFILES/other/automator/Index.workflow" \
		"$HOME/Library/Services/Index.workflow"
ln -siv "$DOTFILES/other/automator/New Note.workflow" \
		"$HOME/Library/Services/New Note.workflow"

# Terminal
# ========

# profile's path and name
p_file=$(find $DOTFILES/other -maxdepth 1 -name "*.terminal" | head -n 1)
p_name=$(basename $p_file .terminal)
open -g $p_file # add profile to terminal app

# default Terminal profile
defaults write com.apple.Terminal "Default Window Settings" "$p_name"
defaults write com.apple.Terminal "Startup Window Settings" "$p_name"
# line marks
defaults write com.apple.Terminal ShowLineMarks -bool false

# Finder
# ======

# set Home directory as the default location for new Finder windows
defaults write com.apple.finder NewWindowTarget 'PfHm'
defaults write com.apple.finder NewWindowTargetPath "file://${HOME}/"
# when performing a search, search the current folder by default
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"
# show the ~/Library folder
chflags nohidden ~/Library && xattr -d com.apple.FinderInfo ~/Library
# show path bar
defaults write com.apple.finder ShowPathbar -bool true
# avoid creating .DS_Store files on network volumes
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
# keep folders on top when sorting by name
defaults write com.apple.finder _FXSortFoldersFirst -bool true
defaults write com.apple.finder _FXSortFoldersFirstOnDesktop -bool true
# enable snap-to-grid for icons on the desktop and in other icon views
/usr/libexec/PlistBuddy -c "Set :DesktopViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist
/usr/libexec/PlistBuddy -c "Set :StandardViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist
# use list view in all Finder windows by default
defaults write com.apple.finder FXPreferredViewStyle -string "Nlsv"

# TextEdit
# ========

# use plain text mode for new TextEdit documents
defaults write com.apple.TextEdit RichText -int 0
# plain text font
defaults write com.apple.TextEdit NSFixedPitchFont -string "SFMono-Regular"
defaults write com.apple.TextEdit NSFixedPitchFontSize -int 14

# Safari
# ======

# enable the Develop menu and the Web Inspector
defaults write com.apple.Safari IncludeDevelopMenu -bool true
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true

# Kill affected applications
# ==========================

for app in \
    "ControlStrip" \
	"Dock" \
	"Finder" \
	"Safari" \
	"TextEdit" \
	"SystemUIServer" \
	"cfprefsd"; do
	killall "${app}" &> /dev/null
done
