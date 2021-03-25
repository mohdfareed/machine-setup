# Dotfiles

## Installation Process

**0. Setup FileVault:**

**1. Run installation script:**

```sh
zsh -c "$(curl -fsSL https://git.io/Jmd2z)"
```

**2. Set login applications:**

- Swish
- Mos
- MonitorControl
- Magnet
- Amphetamine
- OpenInTerminal

**3. Change preferences:**

- System Preferences ->
  - Displays ->
    - Display -> Set external display's resolution scaling
    - Arrangement -> Set external as main
  - Internet Accounts: add Google and University as mail accounts
  - Language & Region -> 24-Hour Time: true
  - Dock & Menu Bar -> Spotlight -> Show in Menu Bar: false
  - Software Update -> Automatically keep Mac up to date
  - Keyboard -> Shortcuts
    - Launchpad -> Show Launchpad: `⌃⇧↓`
    - Mission Control -> Show Desktop: `⌃⇧↑`
    - Services: choose services
  - Extensions -> setup extensions
- Finder ->
  - Sidebar: choose items
  - Tags: uncheck all tags
  - Toolbar: customize
- Safari -> Extensions -> choose extensions (dark reader, IINA, Wipr)
  - Setup Dashlane: Sign-in, enable Touch ID, and background refresh
- OpenInTerminal -> General ->
  - Hide Status Bar Icon: true
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
- Mos -> Exceptions -> Terminal and Parallels Desktop
- Amphetamine ->
  - Triggers -> Enable Triggers: true
  - Add "Closed-Lid Mode":
    - Display count > 0 (External)
    - Battery charge >15% + power adapted is not connected
    - Allow display to sleep

**4. Install applications:**

- Parallels Desktop
  - Setup Windows, Linux, and macOS virtual machines with snapshots
- iA Writer
- Microsoft Office

**5. Setup Time Machine:**

## Miscellaneous

- [Hachidori](https://malupdaterosx.moe/hachidori/)
  - Start Auto Scrobble at launch
  - Set newly scrobbled titles to private
- [Shukofukurou](https://malupdaterosx.moe/shukofukurou-for-macos/)

## Caveats

- Dotfiles and dev directories have to be changed in both `zshenv` and `setup.sh`
- GitHub authentication info might need to be updated in `setup.sh`

## Decommissioning Process

- Backup terminal profile to `dotfiles/other`
- Check installed formulae, casks, and apps and add them to their respective scripts
- Review changes to the apps and system preferences to include in scripts
- Choose the changes to the dotfiles to push.
- Backup virtual machines

## TODO

- Create missing directories when needed.
- Set applications icons
- Find Keka preferences file
- Set desktop wallpaper
- Look into pyenv
- Test preferences
- Setup Fork then continue down AppCleaner list
- Download music with video
