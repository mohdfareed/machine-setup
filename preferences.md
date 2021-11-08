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
  - Spotlight -> Show Spotlight Search: Disable
  - Services->
    - Text -> Disable all
    - Files and Folders -> Disable all
- Extensions -> setup extensions
- Language & Region -> 24-Hour Time: true
- Software Update -> Automatically keep Mac up to date

## Finder

- View Options: Calculate all sizes
- General: New Finder windows show: iCloud Drive

## Safari

- Advanced ->
  - Show Develop menu in menu bar: Enable
  - Save articles for offline reading automatically: Enable
- Extensions -> choose the following:
  - Dark Reader
  - Wiper 1..3

```sh
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true
defaults write com.apple.Safari com.apple.Safari.ContentPageGroupIdentifier.WebKit2DeveloperExtrasEnabled -bool true
```

## Mos

After setting up the app initially, run the script:

```sh
osascript -e 'tell application "Mos" to quit'
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

**Exceptions:** Terminal, Parallels Desktop

## IINA

```sh
osascript -e 'tell application "IINA" to quit'
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
```

Utilities -> Set IINA as the Default Application

## Swish

```sh
osascript -e 'tell application "Swish" to quit'
# show tooltip when performing an action
defaults write co.highlyopinionated.swish tooltipSize -int 4
# resize adjacent window when two windows are snapped next to each other
defaults write co.highlyopinionated.swish snappingResizeAdjacent -bool false
# list of available actions
defaults write co.highlyopinionated.swish actions -string '["menubarAppSwitcher","snapMax","spacesMove","snapCenter","snapQuarters","appNewTab","appQuit","snapHalves"]'
```

## Transmission

```sh
osascript -e 'tell application "Transmission" to quit'
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

## Amphetamine

- Session Defaults ->
    <!--- end session when Mac is forced to sleep -->
  - Forced Sleep: Enable
    <!--- Allow system sleep when display is closed -->
  - Closed-Display Mode: Disable
    <!--- End session if charge (%) is below 10% -->
  - Battery: Enable
    <!--- Ignore charge (%) if power adapter is connected -->
  - Power Adapter: Enable
- Appearance -> Menu Bar Image -> Pill (outline)

## MonitorControl

- App menu -> Menu Icon: Always hide

## Peek

- General -> Preview size: Large
- Code -> Font: Fira Code, Regular, 14
- Markdown ->
  - Markdown -> MathJax: Enable
  - Syntax Highlighting -> Auto-Detect: Disable

## Other

- OpenInTerminal -> General ->
  - Default Text Editor: Visual Studio Code

- Hachidori -> General ->
  - Start Auto Scrobble at launch
  - Set newly scrobbled titles to private
