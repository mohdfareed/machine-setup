# Dotfiles

## Installation Process

**1. Install Xcode Command Line Tools:**

```sh
xcode-select --install
```

**2. Run installer script:**

```sh
curl -L https://git.io/JqcIh | zsh
```

**2. Use default Terminal profile for man-pages:**

    Delete the manpage profile from Terminal app.

## Decommissioning Process

- Backup terminal profile.
- Check installed formulae, casks, and apps and add them to their respective scripts.
- Choose the changes to the dotfiles to push.
- Review changes to the System Preferences to include in scripts.

## TODO

- Learn how to use *defaults* to record and restore System Preferences and macOS configurations.
