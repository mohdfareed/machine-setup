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

**3. Change preferences:**

- MonitorControl -> Advanced -> Hide OSD: true
- Mos -> Exceptions -> Terminal and Parallels Desktop
- Transmission -> General -> Set Default Application
- Keka ->
  - General -> Set Keka as the default decompressor
  - Compression -> Show file in Finder after compression: false
  - Extraction -> Show content in Finder after extraction: false
  - File Access -> Enable home folder/external volumes access
  - Finder Extension -> Show icons in actions: false
- System Preferences ->
  - Displays ->
    - Display -> Set external display's resolution
    - Arrangement -> Set external as main
  - Internet Accounts: add Google and University as mail accounts
  - Language & Region -> 24-Hour Time: true
  - Dock & Menu Bar -> Spotlight -> Show in Menu Bar: false
  - Security & Privacy -> Unlock with Apple Watch
  - Software Update -> Automatically keep Mac up to date
  - Keyboard -> Shortcuts
    - Launchpad -> Show Launchpad: `⌃⇧↓`
    - Mission Control -> Show Desktop: `⌃⇧↑`
    - Services: choose services
  - Extensions -> setup extensions

**4. Install applications:**

- Parallels Desktop
  - Setup Windows, Linux, and macOS virtual machines with snapshots
- Microsoft Office
- iA Writer

**5. Setup Time Machine:**

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

- Learn how to use *defaults* to record and restore System Preferences and macOS configurations.
- Create missing directories when needed.
- Set applications icons
- Find Keka preferences file
- Set desktop wallpaper
- Look into pyenv
- Test preferences
