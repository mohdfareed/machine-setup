# Dotfiles

## Installation Process

**1. Setup Terminal:**

```sh
$HOME/.dotfiles/terminal_defaults.sh
```

**2. Install Xcode Command Line Tools:**

```sh
xcode-select --install
```

**3. Install Oh My Zsh:**

```sh
sh -c "$(curl -fsSL \
https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

**4. Run the installation script:**

```sh
git clone https://github.com/mohdfareed/dotfiles.git $HOME/.dotfiles
$HOME/.dotfiles/install.sh
```

## Decommissioning Process

- Backup terminal profile.

## TODO

- Learn how to use defaults to record and restore System Preferences and macOS configurations.
- Automate GitHub authentication process.
- Clean home directory and move files to `~/.config`.
- Source `.zshrc` before installing ruby gems.
- Fix Ruby script requiring to reload terminal to install gems.
- Look over VSCode settings starting from workbench (and JSON file).
- Ring bell at prompts.
- Install [Oh My Zsh through a script](https://github.com/ohmyzsh/ohmyzsh/#unattended-install).

```sh
ZSH="$HOME/.dotfiles/oh-my-zsh" sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
```
