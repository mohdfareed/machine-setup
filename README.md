# Dotfiles

## Installation Process

**0. Setup FileVault:**

**1. Sign in to the Mac Apple Store:**

**2. Install Xcode CommandLine Tools:**

Run the following code and wait for the installation to complete.

```sh
xcode-select --install
```

**3. Run installation script:**

Run the following code and follow on-screen instructions.

```sh
zsh -c "$(curl -fsSL https://git.io/Jmd2z)"
```

**4. Set login applications:**

- Swish
- Mos
- MonitorControl
- Magnet
- Amphetamine
- OpenInTerminal

**5. Change preferences:**

- System Preferences ->
  - Displays ->
    - Display -> Set external display's resolution scaling
    - Arrangement -> Set external as main
  - Internet Accounts: add Google and University as mail accounts
  - Keyboard -> Shortcuts
    - Launchpad -> Show Launchpad: `⌃⇧↓`
    - Mission Control -> Show Desktop: `⌃⇧↑`
    - Services: choose services
  - Extensions -> setup extensions
  - *Language & Region -> 24-Hour Time: true
  - *Dock & Menu Bar -> Spotlight -> Show in Menu Bar: false
  - *Software Update -> Automatically keep Mac up to date
- Finder -> Sidebar: customize and remove tags manually
  - Toolbar: customize
- Safari -> Extensions -> choose extensions (dark reader, IINA, Wipr)
  - Setup Dashlane: Sign-in, enable Touch ID, and background refresh
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
- Mos -> Exceptions -> Terminal and Parallels Desktop
- Amphetamine ->
  - Triggers -> Enable Triggers: true
  - Add "Closed-Lid Mode":
    - Display count > 0 (External)
    - Battery charge >15% + power adapted is not connected
    - Allow display to sleep

**6. Install applications:**

- Parallels Desktop
  - Setup Windows, Linux, and macOS virtual machines with snapshots
- iA Writer
- Microsoft Office

**7. Setup Time Machine:**

## Miscellaneous

- [Hachidori](https://malupdaterosx.moe/hachidori/)
  - Start Auto Scrobble at launch
  - Set newly scrobbled titles to private
- [Shukofukurou](https://malupdaterosx.moe/shukofukurou-for-macos/)

## Caveats

- Dotfiles and dev directories have to be changed in both `zshenv` and `setup.sh`.
- Dotfiles directory structure is hardcoded.
- GitHub authentication info might need to be updated in `setup.sh`.
- Changing Homebrew's default directory breaks some `zshrc` functionality.
- Zsh directories are set in both `zsh.sh` and `zshenv`.

## Decommissioning Process

- Backup terminal profile to `dotfiles/other`
- Backup virtual machines
- Choose the changes to preferences and formulae, casks, and apps to push.

## TODO

- Cleanup setup.
- Create missing directories when needed.
- Test preferences
- Setup Fork then continue down AppCleaner list
- Set defaults apps for common file types
- switch from `exa` to `lsd`
