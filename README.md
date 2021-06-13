# Dotfiles

## Installation Process

**0. Setup FileVault:**

**1. Sign in to the Mac Apple Store:**

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

Change OS and application [preferences](preferences.md) manually.

**5. Install applications:**

- Parallels Desktop
  - Setup Windows, Linux, and macOS virtual machines with snapshots
- iA Writer
- Microsoft Office

**6. Setup Time Machine:**

## Miscellaneous

- [Hachidori](https://malupdaterosx.moe/hachidori/)
  - Start Auto Scrobble at launch
  - Set newly scrobbled titles to private
- [Shukofukurou](https://malupdaterosx.moe/shukofukurou-for-macos/)

## Caveats

- Dotfiles and dev directories have to be changed in both `zshenv` and `setup.sh`.
- Dotfiles repository structure is hardcoded.
- GitHub authentication info might need to be updated in `setup.sh`.
- Zsh directories are set in both `zsh.sh` and `zshenv`.

## Decommissioning Process

- Backup terminal profile to `dotfiles/other`
- Backup virtual machines
- Choose the changes to preferences and formulae, casks, and apps to push
