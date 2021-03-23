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

# TODO: Check if needed
# close open System Preferences panes, to prevent them from overriding settings
osascript -e 'tell application "System Preferences" to quit'
# ask for the administrator password upfront
sudo -v

# main
# ====

# trackpad, mouse, and keyboard
# =============================

# tap to click
defaults write com.apple.AppleMultitouchTrackpad Clicking -bool true
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true
# disable mouse acceleration
defaults write NSGlobalDomain com.apple.mouse.scaling -1
# show expanded control strip in touch bar
defaults write com.apple.touchbar.agent PresentationModeGlobal -string fullControlStrip

# Energy Saving
# =============

# TODO: test it
# require password immediately after screen saver begins
defaults write com.apple.screensaver askForPassword -int 1
defaults write com.apple.screensaver askForPasswordDelay -int 0

# TODO: Extensions: com.apple.preferences.extensions....
# ==========

# Terminal
# ========

# profile's path and name
p_file=$(find $DOTFILES/other -maxdepth 1 -name "*.terminal" | head -n 1)
p_name=$(basename $p_file .terminal)
open $p_file # add profile to terminal app
sleep 1 # Wait to make sure the theme is loaded


# set profile as the default
defaults write com.apple.Terminal "Default Window Settings" "$p_name"
defaults write com.apple.Terminal "Startup Window Settings" "$p_name"
# hide line marks
defaults write com.apple.Terminal ShowLineMarks -int 0

# Finder
# ======

# show all filename extensions
defaults write NSGlobalDomain AppleShowAllExtensions -bool true
# when performing a search, search the current folder by default
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"
# use list view in all Finder windows by default
defaults write com.apple.finder FXPreferredViewStyle -string "Nlsv"
# show the ~/Library folder
chflags nohidden ~/Library && xattr -d com.apple.FinderInfo ~/Library

# Safari
# ======

# prevent Safari from opening ‘safe’ files automatically after downloading
defaults write com.apple.Safari AutoOpenSafeDownloads -bool false
# save articles in Reading List for offline reading automatically
defaults write com.apple.Safari ReadingListSaveArticlesOfflineAutomatically -bool true
# enable the Develop menu and the Web Inspector in Safari
defaults write com.apple.Safari IncludeDevelopMenu -bool true
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true

# Swish
# =====

# show app icon in menubar
defaults write co.highlyopinionated.swish showInMenuBar -bool false
# show tooltip when performing an action
defaults write co.highlyopinionated.swish tooltipSize -int 4
# resize adjacent window when two windows are snapped next to each other
defaults write co.highlyopinionated.swish snappingResizeAdjacent -bool false
# list of available actions
defaults write co.highlyopinionated.swish actions -string '["menubarAppSwitcher","snapMax","spacesMove","snapCenter","snapQuarters","appNewTab","appQuit","snapHalves"]'

# Mos
# ===

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

# Transmission
# ============

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
