# Dotfiles

## Installation Process

**1. Install Xcode Command Line Tools:**

```sh
xcode-select --install
```

**2. Run installation script:**

```sh
zsh -c "$(curl -fsSL https://git.io/Jmd2z)"
```

## Decommissioning Process

- Backup terminal profile to `dotfiles/other`.
- Check installed formulae, casks, and apps and add them to their respective scripts.
- Choose the changes to the dotfiles to push.
- Review changes to the apps and system preferences to include in scripts.

## TODO

- Learn how to use *defaults* to record and restore System Preferences and macOS configurations.
- Clean up entire setup
  - Specify which steps are necessary and which are optional.
