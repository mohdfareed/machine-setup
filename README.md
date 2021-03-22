# Dotfiles

## Installation Process

**1. Run installation script:**

```sh
zsh -c "$(curl -fsSL https://git.io/Jmd2z)"
```

## Caveats

- Dotfiles and dev directories have to be changed in both `zshenv` and `setup.sh`.
- GitHub authentication info might need to be updated in `setup.sh`.

## Decommissioning Process

- Backup terminal profile to `dotfiles/other`.
- Check installed formulae, casks, and apps and add them to their respective scripts.
- Choose the changes to the dotfiles to push.
- Review changes to the apps and system preferences to include in scripts.

## TODO

- Learn how to use *defaults* to record and restore System Preferences and macOS configurations.
