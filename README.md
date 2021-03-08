# Dotfiles

## Installation

1. Install Xcode Command Line Tools

```sh
$ xcode-select --install
```

2. Install Oh My Zsh

```sh
$ sh -c "$(curl -fsSL \
      https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

3. Run the installation script

```sh
$ git clone https://github.com/mohdfareed/dotfiles.git ~/.dotfiles
$ $HOME/.dotfiles/install.sh
```

## TODO

- Learn how to use defaults to record and restore System Preferences and other macOS configurations.
- Write more detailed bootstrapping steps.
- Make a checklist of steps to decommission your computer before wiping your hard drive.
- Modify packages and applications installed by default.
- Automate GitHub authentication process.
- Set specific setup scripts for Ruby and other frameworks.
- Add update script
