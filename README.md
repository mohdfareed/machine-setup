# Dotfiles

## Installation Process

**1. Run installation script:**

```sh
zsh -c "$(curl -fsSL https://git.io/Jmd2z)"
```

**2. Set login applications:**

- Swish
- Mos
- MonitorControl
- Magnet

**3. Change some preferences manually:**

- MonitorControl -> Advanced -> Hide OSD: true
- Mos -> Exceptions -> Terminal and Parallels Desktop
- Transmission -> General -> Set Default Application

- Keka -> General -> Set Keka as the default decompressor
- Keka -> Compression -> Show file in Finder after compression: false
- Keka -> Extraction -> Show content in Finder after extraction: false
- Keka -> File Access -> Enable home folder/external volumes access
- Keka -> Finder Extension -> Show icons in actions: false

- System Preferences -> Displays -> Display -> Set external display's resolution
- System Preferences -> Displays -> Arrangement -> Set external as main

**4. Install come applications manually:**

- Parallels Desktop
  - Setup Windows, Linux, and macOS virtual machines with snapshots
- Microsoft Office (optional)
- iA Writer

## Caveats

- Dotfiles and dev directories have to be changed in both `zshenv` and `setup.sh`
- GitHub authentication info might need to be updated in `setup.sh`

## Decommissioning Process

- Backup terminal profile to `dotfiles/other`
- Check installed formulae, casks, and apps and add them to their respective scripts
- Review changes to the apps and system preferences to include in scripts
- Choose the changes to the dotfiles to push.
- Backup virtual machines

## TODO

- Learn how to use *defaults* to record and restore System Preferences and macOS configurations.
- Create missing directories when needed.
- Set applications icons
- Find Keka preferences file
