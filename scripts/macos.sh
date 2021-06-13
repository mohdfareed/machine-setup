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
open $p_file # add profile to terminal app

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

# FIXME: Doesn't work
# Safari
# ======
open -Wga Safari
echo "${bold}Exit Safari to continue...${clear}"

# open ‘safe’ files automatically after downloading
defaults write com.apple.Safari AutoOpenSafeDownloads -bool false
# save articles in Reading List for offline reading automatically
defaults write com.apple.Safari ReadingListSaveArticlesOfflineAutomatically -bool true
# enable the Develop menu and the Web Inspector
defaults write com.apple.Safari IncludeDevelopMenu -bool true
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true

# IINA
# ====

echo $(brew list) | grep -q " iina "
if [[ $? = 0 ]] ; then
	open -a IINA

	# quit after all windows are closed
	defaults write com.colliderli.iina quitWhenNoOpenedWindow -bool true
	# match system appearance
	defaults write com.colliderli.iina themeMaterial -int 4
	# set on screen controller toolbar items
	defaults write com.colliderli.iina controlBarToolbarButtons -array \
		-int 4 \
		-int 2 \
		-int 1 \
		-int 0
	# use left/right button for previous/next media
	defaults write com.colliderli.iina arrowBtnAction -int 1
	# show chapter position in progress bar
	defaults write com.colliderli.iina showChapterPos -bool true
	# show remaining time instead of total duration
	defaults write com.colliderli.iina showRemainingTime -bool true
	# preferred subtitles language
	defaults write com.colliderli.iina subLang -string "en"
	# custom youtube-dl path
	defaults write com.colliderli.iina ytdlSearchPath -string "/usr/local/bin"
fi

# Swish
# =====

echo $(brew list) | grep -q " swish "
if [[ $? = 0 ]] ; then
	# show tooltip when performing an action
	defaults write co.highlyopinionated.swish tooltipSize -int 4
	# resize adjacent window when two windows are snapped next to each other
	defaults write co.highlyopinionated.swish snappingResizeAdjacent -bool false
	# list of available actions
	defaults write co.highlyopinionated.swish actions -string '["menubarAppSwitcher","snapMax","spacesMove","snapCenter","snapQuarters","appNewTab","appQuit","snapHalves"]'
fi

# FIXME: Doesn't work
# Mos
# ===

echo $(brew list) | grep -q " mos "
if [[ $? = 0 ]] ; then
	open -Wga mos
	echo "${bold}Exit Mos to continue...${clear}"

	# reverse the mouse wheel scroll direction
	defaults write com.caldis.Mos reverse -bool false
	# hide menubar icon. Re-run Mos again to show the hidden icon
	defaults write com.caldis.Mos hideStatusItem -bool true
	# sets the minimum scroll distance
	defaults write com.caldis.Mos step -float 78
	# sets the scrolling acceleration
	defaults write com.caldis.Mos speed -float 1
	# sets the duration of the scroll animation
	defaults write com.caldis.Mos duration -float 2
fi

# FIXME: Doesn't work
# Transmission
# ============
echo $(brew list) | grep -q " transmission "
if [[ $? = 0 ]] ; then
	open -Wga transmission
	echo "${bold}Exit Transmission to continue...${clear}"

	# automatically size windows to fit all transfers
	default write org.m0k.transmission AutoSize -bool true
	# show total upload rate badge on dock icon
	default write org.m0k.transmission BadgeDownloadRate -bool true
	# show total upload rate badge on dock icon
	default write org.m0k.transmission BadgeUploadRate -bool false
	# prompt for removal of active transfers only when downloading
	default write org.m0k.transmission CheckRemoveDownloading -bool true
	# prompt for quitting with active transfers only when downloading
	default write org.m0k.transmission CheckQuitDownloading -bool true
	# display a window when opening torrent files only when there are multiple files
	default write org.m0k.transmission DownloadAskMulti -bool true
	# display a window when opening a magnet link
	default write org.m0k.transmission MagnetOpenAsk -bool true
	# download to DownloadFolder instead of the location of the torrent file
	default write org.m0k.transmission DownloadLocationConstant -bool true
	# the default download location
	default write org.m0k.transmission DownloadFolder -string "$HOME/Downloads"
fi

# Kill affected applications
# ==========================

for app in \
    "ControlStrip" \
	"Dock" \
	"Finder" \
	"Safari" \
	"Transmission" \
	"Swish" \
	"Mos" \
	"IINA" \
	"TextEdit" \
	"SystemUIServer" \
	"cfprefsd"; do
	killall "${app}" &> /dev/null
done
