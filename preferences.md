# Preferences

The following are OS and application preferences that are done manually.

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

- Safari -> Extensions -> choose the following:
  - Dark Reader/Dark Mode for Safari
  - Wiper 1..3
  - Dashlane: Sign-in, enable Touch ID, and background refresh then disable

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

## Other

- OpenInTerminal -> General ->
  - Default Text Editor: Visual Studio Code

- Transmission -> General -> Set Default Application

- Keka ->
  - General -> Set Keka as the default decompressor
  - Compression -> Show file in Finder after compression: false
  - Extraction -> Show content in Finder after extraction: false
  - File Access -> Enable home folder/external volumes access
  - Finder Extension -> Show icons in actions: false

- IINA -> Utilities -> Set IINA as the Default Application

- MonitorControl -> Advanced -> Hide OSD: true

- Amphetamine ->
  - Triggers -> Enable Triggers: true
  - Add "Closed-Lid Mode":
    - Display count > 0 (External)
    - Battery charge >15% + power adapted is not connected
    - Allow display to sleep
