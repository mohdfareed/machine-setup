# Dotfiles

## Installation Process

**1. Install Xcode Command Line Tools:**

```sh
xcode-select --install
```

**2. Pull Dotfiles repo:**

```sh
git clone https://github.com/mohdfareed/dotfiles.git $HOME/.dotfiles
```

**3. Setup Terminal:**

```sh
$HOME/.dotfiles/terminal_setup.sh
```

**4. Run the installation script:**

```sh
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
