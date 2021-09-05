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

### asdf

Sets up `asdf`, version manager for multiple runtimes.

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
- [Batteries for Mac](https://www.fadel.io/batteries)
  - Show battery level of devices on the same network
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

## Caveats

- XDG base directories are set following the [GO implementation](https://github.com/adrg/xdg)
- Dotfiles directory is set in both `zshenv` and `bootstrap.sh`
- Dotfiles repository structure is hardcoded
- GitHub PAT might need to be updated in `bootstrap.sh`
- `bootstrap.sh` link in README might need to be updated

## Decommissioning Process

- Backup terminal profile to `dotfiles/macos`
- Backup `gpg` and `ssh` keys
- Backup virtual machines
- Choose the changes to preferences and formulae, casks, and apps to push
- Sign out from the device and Find My app

## TODO

- Input passphrase for `gpg` key through a script
