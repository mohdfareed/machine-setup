#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up macOS Preferences...${clear}"

# check if dotfiles repo exists
if [[ ! -d $DOTFILES ]] ; then
    echo "${rbold}Error:${clear} DOTFILES directory does not exist..."
    return 1
fi

source $DOTFILES/dots/zshenv
# create link to personal music in Music folder
ln -siv $iCloud/Music $HOME/Music/Personal
# close open System Preferences panes, to prevent them from overriding settings
osascript -e 'tell application "System Preferences" to quit'
# ask for the administrator password upfront
sudo -v

# General
# =======

# set computer name and local host name
scutil --set ComputerName "Mohd's MacBook Pro"
scutil --set LocalHostName "Mohds-MacBook-Pro"
# prefer tabs when opening documents
defaults write .GlobalPreferences AppleWindowTabbingMode -string "always"
# allow wallpaper tinting in windows
defaults write .GlobalPreferences AppleReduceDesktopTinting -bool true
# when switching to an application, switch to a space with open windows
defaults write .GlobalPreferences AppleSpacesSwitchOnActivate -bool false
# automatically rearrange spaces based on most recent use
defaults weire com.apple.dock mru-spaces -bool false
# Automatically hide and show the Dock
defaults write com.apple.dock autohide -bool true
# Play feedback when volume is changed
defaults write .GlobalPreferences com.apple.sound.beep.feedback -bool true
# set desktop wallpaper
wp=$(find $DOTFILES/other -maxdepth 1 -name "wallpaper.*" | head -n 1)
osascript -e "tell application \"Finder\" to set desktop picture to POSIX file \"$wp\""
osascript -e 'tell application "Finder" to set desktop picture to POSIX file "$wp"'

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

# show input menu in menu bar
defaults write com.apple.TextInputMenu visible -bool true
# Show input menu in the login screen
sudo defaults write /Library/Preferences/com.apple.loginwindow showInputMenu -bool true
# touch bar global presentation mode
defaults write com.apple.touchbar.agent PresentationModeGlobal -string "fullControlStrip"
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

# Extensions
# ==========

# add workflows
open "$DOTFILES/other/automator/Index.workflow"
open "$DOTFILES/other/automator/New Note.workflow"

# Terminal
# ========

# profile's path and name
p_file=$(find $DOTFILES/other -maxdepth 1 -name "*.terminal" | head -n 1)
p_name=$(basename $p_file .terminal)
open $p_file # add profile to terminal app
sleep 1 # Wait to make sure the theme is loaded

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
# set toolbar items
defaults write com.apple.finder "NSToolbar Configuration Browser" '{
    "TB Item Identifiers" =     (
        "com.apple.finder.BACK",
        NSToolbarFlexibleSpaceItem,
        "com.apple.finder.SWCH",
        NSToolbarSpaceItem,
        "com.apple.finder.ARNG",
        "com.apple.finder.NFLD",
        "com.apple.finder.TRSH",
        "wang.jianing.app.OpenInTerminal.OpenInTerminalFinderExtension",
        NSToolbarSpaceItem,
        "com.apple.finder.SRCH"
    );
    "TB Display Mode" = 2;
}'
killall Finder
# Avoid creating .DS_Store files on network volumes
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
# Keep folders on top when sorting by name
defaults write com.apple.finder _FXSortFoldersFirst -bool true
defaults write com.apple.finder _FXSortFoldersFirstOnDesktop -bool true
# Enable snap-to-grid for icons on the desktop and in other icon views
/usr/libexec/PlistBuddy -c "Set :DesktopViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist
/usr/libexec/PlistBuddy -c "Set :FK_StandardViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist
/usr/libexec/PlistBuddy -c "Set :StandardViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist
# show preview pane
defaults write com.apple.finder ShowPreviewPane -bool true
# use list view in all Finder windows by default
defaults write com.apple.finder FXPreferredViewStyle -string "Nlsv"
# default list view settings
defaults write com.apple.finder FK_DefaultListViewSettings '{
    calculateAllSizes = 1;
    columns = (
        {
            ascending = 1;
            identifier = name;
            visible = 1;
        },
        {
            ascending = 1;
            identifier = size;
            visible = 1;
        },
        {
            ascending = 1;
            identifier = kind;
            visible = 1;
        }
    );
    showIconPreview = 1;
    sortColumn = name;
    useRelativeDates = 1;
    viewOptionsVersion = 1;
}'

# Safari
# ======

# open ‘safe’ files automatically after downloading
defaults write com.apple.Safari AutoOpenSafeDownloads -bool false
# save articles in Reading List for offline reading automatically
defaults write com.apple.Safari ReadingListSaveArticlesOfflineAutomatically -bool true
# enable the Develop menu and the Web Inspector
defaults write com.apple.Safari IncludeDevelopMenu -bool true
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true

# TextEdit
# ========

# use plain text mode for new TextEdit documents
defaults write com.apple.TextEdit RichText -int 0
defaults write com.apple.TextEdit NSFixedPitchFont -string "SFMono-Regular"
defaults write com.apple.TextEdit NSFixedPitchFontSize -int 14

# Calendar
# ========

# show events in year view
defaults write com.apple.iCal "Show heat map in Year View" -bool true

# Transmission
# ============
brew casks | grep -q "^transmission$"
if [[ $? = 0 ]] ; then
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
	default write org.m0k.transmission DownloadFolder -string $HOME/Downloads
fi

# IINA
# ====

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

# Swish
# =====
brew casks | grep -q "^swish$"
if [[ $? = 0 ]] ; then
	# show app icon in menubar
	defaults write co.highlyopinionated.swish showInMenuBar -bool false
	# show tooltip when performing an action
	defaults write co.highlyopinionated.swish tooltipSize -int 4
	# resize adjacent window when two windows are snapped next to each other
	defaults write co.highlyopinionated.swish snappingResizeAdjacent -bool false
	# list of available actions
	defaults write co.highlyopinionated.swish actions -string '["menubarAppSwitcher","snapMax","spacesMove","snapCenter","snapQuarters","appNewTab","appQuit","snapHalves"]'
fi

# Mos
# ===

brew casks | grep -q "^mos$"
if [[ $? = 0 ]] ; then
	# reverse the mouse wheel scroll direction
	defaults write com.caldis.Mos reverse -bool 0
	# hide menubar icon. Re-run Mos again to show the hidden icon
	defaults write com.caldis.Mos hideStatusItem -bool 1
	# sets the minimum scroll distance
	defaults write com.caldis.Mos step -float 78
	# sets the scrolling acceleration
	defaults write com.caldis.Mos speed -float 1
	# sets the duration of the scroll animation
	defaults write com.caldis.Mos duration -float 2
fi

# Kill affected applications
# ==========================

for app in "ControlStrip" \
	"Calendar" \
	"cfprefsd" \
	"Dock" \
	"Finder" \
	"Safari" \
	"SystemUIServer" \
	"Terminal" \
	"Transmission" \
	"Swish" \
	"Mos" \
	"IINA" \
	"TextEdit"; do
	killall "${app}" &> /dev/null
done
