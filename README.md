# Dotfiles

## Installation

**Setup FileVault:**

**Sign in to the App Store:**

**Install Xcode CommandLine Tools:**

```sh
xcode-select --install
```

**Run the bootstrap script:**

```sh
zsh -c "$(curl -fsSL https://git.io/JX4FH)"
```

**Setup Time Machine:**

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
- Setup update scripts
