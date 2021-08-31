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

## zsh

Installs `zsh` and `oh-my-zsh`, creates needed directories, links configuration files and theme, and cleans up home directory.

Required environment variables:

- `$ZSH`
- `$ZDOTDIR`
- `$ZSH_COMPDUMP`
- `$HISTFILE`

## git

Installs `git`, `gpg`, and `pinentr-mac` through HomeBrew, links configuration files, and imports commits signing key.

Required environment variables:

- `$XDG_CONFIG_HOME`
- `$GNUPGHOME`

The passphrase for the key is printed before importing the key.

## asdf

Installs `asdf` and links configuration file.

Required environment variables:

- `$ASDF_CONFIG_FILE`

## python

Links python's startup file and installs latest python through `asdf`. Startup files manages python's interactive shell's history file.

Required environment variables:

- `$PYTHONSTARTUP`

## ruby

Installs latest ruby through `asdf` with some gems.

## node

Creates directories needed by `npm` and `REPL` and installs latest node though `asdf`.

Required environment variables:

- `$NPM_CONFIG_USERCONFIG`
- `$NPM_CONFIG_CACHE`
- `$NODE_REPL_HISTORY`

## databases

Sets up `sqlite` and `postgresql`.

### sqlite

Creates history directory and installs latest sqlite through `asdf`.

### postgresql

Creates needed directories and installs latest postgresql through `asdf`. It sets the variables `$POSTGRES_EXTRA_CONFIGURE_OPTIONS` to compile with `openssl` libraries.

Required environment variables:

- `$PSQLRC`
- `$PSQL_HISTORY`

## Miscellaneous

- [Hachidori](https://malupdaterosx.moe/hachidori/)
  - Start Auto Scrobble at launch
  - Set newly scrobbled titles to private
- [Shukofukurou](https://malupdaterosx.moe/shukofukurou-for-macos/)

## Caveats

- Dotfiles directory is set in both `zshenv` and `bootstrap.sh`.
- Dotfiles repository structure is hardcoded.
- GitHub authentication info might need to be updated in `bootstrap.sh`.

## Decommissioning Process

- Backup terminal profile to `dotfiles/resources`.
- Backup gpg and ssh keys.
- Backup virtual machines.
- Choose the changes to preferences and formulae, casks, and apps to push.
- Sign out from the device and Find My app.

## TODO

- Input passphrase for gpg key through script
- Add extra script for unnecessary setup
- Run unnecessary scripts manually
- Add unnecessary testing scripts to use in extra scripts
