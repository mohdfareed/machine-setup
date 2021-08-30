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

## Scripts

### git

Installs `git`, `gpg`, and `pinentr-mac` through HomeBrew, links configuration files, and imports commits signing key.

Required environment variables:

- `$DOTFILES`
- `$XDG_CONFIG_HOME` - sourced within the script through zshenv
- `$GNUPGHOME` - sourced within the script through zshenv

The paths to the dotfiles and the signing key and its owner trust are hardcoded. The passphrase for the key is printed before importing the key.

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

- Add extra script for unnecessary setup
- Run unnecessary scripts manually
- Add unnecessary testing scripts to use in extra scripts
