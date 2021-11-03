# Dotfiles

## Installation

**0. Setup FileVault:**

**1. Sign in to the App Store:**

**2. Install Xcode CommandLine Tools:**

```sh
xcode-select --install
```

**3. Run the bootstrap script:**

```sh
zsh -c "$(curl -fsSL https://git.io/JEQad)"
```

**4. Setup Time Machine:**

## Scripts

### homebrew

Installs HomeBrew along with formulae, casks, and fonts.

### zsh

Sets up `zsh` and `oh-my-zsh`. Requires HomeBrew.

### git

Sets up `git` along with a `gpg` signing key. Requires HomeBrew.  
The passphrase is printed before importing the key.

### appstore

Installs `mas` and select apps from the App Store. Requires HomeBrew and to be signed in to the App Store.

### macos

Sets basic macOS preferences.

### [Raycast](https://github.com/mohdfareed/raycast.git)

Private repo is cloned. Configuration in repo must be imported in Raycast.

### asdf

Sets up `asdf`, version manager for multiple runtimes. The data directory is set manually because it cannot contain white space.

### python

Links python's startup file and installs the latest Python through `asdf`. The startup file manages python's interactive shell's history file.

### ruby

Installs latest Ruby through `asdf` with some gems.

### node

Creates directories needed by `npm` and `REPL` and installs the latest Node.js through `asdf`.

### databases

Sets up `sqlite` and `postgresql`.

#### sqlite

Creates history directory and installs latest SQLite through `asdf`.

#### postgresql

Installs latest PostgreSQL through `asdf`. It sets the variables `$POSTGRES_EXTRA_CONFIGURE_OPTIONS` to compile with `openssl` libraries.

## Miscellaneous

- [AppCleaner](https://freemacsoft.net/appcleaner/)
  - Application uninstaller
  - `brew install --cask appcleaner`
- [Telegram](https://macos.telegram.org)
  - Messaging app with a focus on speed and security
  - `brew install --cask telegram`
- [Hachidori](https://malupdaterosx.moe/hachidori/)
  - Updates anime list automatically while watching
- [Shukofukurou](https://malupdaterosx.moe/shukofukurou-for-macos/)
  - Manages Anime and Manga AniList and MyAnimeList lists
- [Keka](https://www.keka.io/)
  - File archiver and unarchiver
- [Fork](https://git-fork.com/)
  - macOS native GIT client
- [Google Chrome](https://www.google.com/chrome/)
  - Web browser
- [Stats](https://github.com/exelban/stats)
  - System monitor for the menu bar
- [Grok](https://www.trygrok.com)
  - Code-centric documentation in VSCode
- [Peek](https://www.bigzlabs.com/peek.html)
  - Quick Look extension
  - Better Markdown handling (MathJax support)
  - Lacks `.zip` support
- [Minimalist](https://minimalistpassword.com/)
  - Fully native password manager
- [Elpass](https://elpass.app/)
  - Free password manager
- [Batteries](https://www.fadel.io/batteries)
  - Tracks all your devices' batteries from your Mac
- [Dash](https://kapeli.com/dash)
  - API Documentation Browser and Code Snippet Manager
- [Dropover](https://dropoverapp.com)
  - Stash, gather or move any draggable content
- [TextSniper](https://textsniper.app)
  - Extract text from images and other digital documents
- [Calca](http://calca.io)
  - Symbolic calculator with built-in grapher
- [Peek](https://www.bigzlabs.com/peek.html)
  - Code and Markdown quicklook extension
- [HyperDock](https://bahoom.com/hyperdock)
  - Window preview in dock
- [TopNotch](https://topnotch.app)
  - Hide notch on MacBook Pro
- [Termius](https://termius.com)
  - macOS and iOS SSH client.
- [TablePlus](https://tableplus.com)
  - Native database client.
- [Rectangle](https://rectangleapp.com)
  - macOS window manager.
- [AltTab](https://alt-tab-macos.netlify.app)
  - Windows switcher with preview.

## Caveats

- XDG base directories are set following the [GO implementation](https://github.com/adrg/xdg)
- Dotfiles directory is set in both `zshenv` and `bootstrap.sh`
- Dotfiles repository structure is hardcoded
- GitHub PAT might need to be updated in `bootstrap.sh`
- `bootstrap.sh` link in README might need to be updated
- macOS script sets up Raycast which requires git authentication

## Decommissioning Process

- Backup terminal profile to `dotfiles/macos`
- Backup `gpg` and `ssh` keys
- Backup virtual machines
- Choose the changes to preferences and formulae, casks, and apps to push
- Sign out from the device and Find My app

## TODO

- Input passphrase for `gpg` key through a script
- Setup update scripts
