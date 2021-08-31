# Dotfiles

## Installation

**0. Setup FileVault:**

**1. Sign in to the App Store:**

**2. Install Xcode CommandLine Tools:**

Run the following code and wait for the installation to complete.

```sh
xcode-select --install
```

**3. Run setup script:**

Run the following code and follow on-screen instructions.

```sh
zsh -c "$(curl -fsSL https://git.io/JZbBu)"
```

**4. Change preferences:**

Change OS and applications [preferences](preferences.md) manually.

**5. Install applications:**

- Parallels Desktop
  - Setup Windows, Linux, and macOS virtual machines with snapshots
- iA Writer
- Microsoft Office

**6. Setup Time Machine:**

## homebrew

Installs HomeBrew along with formulae, casks, and fonts.

## zsh

Sets up `zsh` and `oh-my-zsh`. Requires HomeBrew.

## git

Sets up `git` along with a `gpg` signing key. Requires HomeBrew.  
The passphrase is printed before importing the key.

## appstore

Installs `mas` and select apps from the App Store. Requires HomeBrew and to be signed in to the App Store.

## macos

Sets basic macOS preferences.

## asdf

Sets up `asdf`, version manager for multiple runtimes.

## python

Links python's startup file and installs latest python through `asdf`. Startup files manages python's interactive shell's history file.

## ruby

Installs latest ruby through `asdf` with some gems.

## node

Creates directories needed by `npm` and `REPL` and installs latest node though `asdf`.

## databases

Sets up `sqlite` and `postgresql`.

### sqlite

Creates history directory and installs latest sqlite through `asdf`.

### postgresql

Installs latest postgresql through `asdf`. It sets the variables `$POSTGRES_EXTRA_CONFIGURE_OPTIONS` to compile with `openssl` libraries.

## Miscellaneous

- [AppCleaner](https://freemacsoft.net/appcleaner/)
  - Application uninstaller
  - `brew install --cask appcleaner`
- [Telegram](https://macos.telegram.org)
  - Messaging app with a focus on speed and security
  - `brew install --cask telegram`
- [Hachidori](https://malupdaterosx.moe/hachidori/)
  - Updates anime list automatically while watching
  - Start Auto Scrobble at launch
  - Set newly scrobbled titles to private
- [Shukofukurou](https://malupdaterosx.moe/shukofukurou-for-macos/)
  - Manages Anime and Manga AniList and MyAnimeList lists

## Caveats

- Dotfiles directory is set in both `zshenv` and `bootstrap.sh`.
- Dotfiles repository structure is hardcoded.
- GitHub PAT might need to be updated in `bootstrap.sh`.
- `bootstrap.sh` link in README might need to be updated.

## Decommissioning Process

- Backup terminal profile to `dotfiles/resources`.
- Backup `gpg` and `ssh` keys.
- Backup virtual machines.
- Choose the changes to preferences and formulae, casks, and apps to push.
- Sign out from the device and Find My app.

## TODO

- Input passphrase for gpg key through script
