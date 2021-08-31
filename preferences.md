# Preferences

The following are OS and application preferences that are set manually.

## Login Applications

- Swish
- Mos
- MonitorControl
- Magnet
- Amphetamine
- OpenInTerminal

## System Preferences

- Keyboard -> Shortcuts ->
  - Launchpad -> Show Launchpad: `⌃⇧↓`
  - Mission Control -> Show Desktop: `⌃⇧↑`
  - Services->
    - Text -> Disable all
    - Files and Folders:
      - Index
      - New Note
- Extensions -> setup extensions
- Language & Region -> 24-Hour Time: true
- Software Update -> Automatically keep Mac up to date

## Finder

- View Options: Calculate all sizes

## Safari

- Extensions -> choose the following:
  - Dark Reader
  - Wiper 1..3

## Mos

After setting up the app initially, run the script:

```sh
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
```

## IINA

```sh
echo $(brew list) | grep -q " iina "
if [[ $? = 0 ]] ; then
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
```

Utilities -> Set IINA as the Default Application

## Swish

```sh
echo $(brew list) | grep -q " swish "
if [[ $? = 0 ]] ; then
 # show tooltip when performing an action
 defaults write co.highlyopinionated.swish tooltipSize -int 4
 # resize adjacent window when two windows are snapped next to each other
 defaults write co.highlyopinionated.swish snappingResizeAdjacent -bool false
 # list of available actions
 defaults write co.highlyopinionated.swish actions -string '["menubarAppSwitcher","snapMax","spacesMove","snapCenter","snapQuarters","appNewTab","appQuit","snapHalves"]'
fi
```

## Transmission

```sh
# automatically size windows to fit all transfers
defaults write org.m0k.transmission AutoSize -bool true
# show total upload rate badge on dock icon
defaults write org.m0k.transmission BadgeDownloadRate -bool true
# show total upload rate badge on dock icon
defaults write org.m0k.transmission BadgeUploadRate -bool false
# prompt for removal of active transfers only when downloading
defaults write org.m0k.transmission CheckRemoveDownloading -bool true
# prompt for quitting with active transfers only when downloading
defaults write org.m0k.transmission CheckQuitDownloading -bool true
# display a window when opening torrent files only when there are multiple files
defaults write org.m0k.transmission DownloadAskMulti -bool true
# display a window when opening a magnet link
defaults write org.m0k.transmission MagnetOpenAsk -bool true
# download to DownloadFolder instead of the location of the torrent file
defaults write org.m0k.transmission DownloadLocationConstant -bool true
# the default download location
defaults write org.m0k.transmission DownloadFolder -string "$HOME/Downloads"
```

- General -> Set Default Application

## Other

- OpenInTerminal -> General ->
  - Default Text Editor: Visual Studio Code

- MonitorControl -> Advanced -> Hide OSD: true

- Amphetamine ->
  - Triggers -> Enable Triggers: true
  - Add "Closed-Lid Mode":
    - Display count > 0 (External)
    - Battery charge >15% + power adapted is not connected
    - Allow display to sleep

- Hachidori -> General ->
  - Start Auto Scrobble at launch
  - Set newly scrobbled titles to private
