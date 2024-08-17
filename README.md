# Machine

This is a Python project that provides a collection of modules for
setting up various aspects of a machine, along with a library of utility
modules that are used throughout the project.

## Usage

To set up the machine, run the following command:

```sh
url=https://raw.githubusercontent.com/mohdfareed/machine/main/bootstrap.py
curl -fsSL $url | python3 - [-f|--force] [-h|--help]
```

Where the arguments are as follows:

- `-f|--force`: forces cloning the repo even if it already exists.
- `-h|--help`: prints the help message.

### Individual Setup

Individual machine components can be set up by running the respective setup
module, provided that the bootstrapping script has already been run. Run the
following command to set up a component:

```sh
python -m scripts.[component] [-h]
```

### Updating and Cleaning

To update the machine, reapplying setup config, run the following command:

```sh
python -m scripts.[machine] [-h]
```

## Configuration

The common configuration that is shared across all machines. All machines must
have the configuration below.

### Files

- `$PRIVATE_MACHINE/env.sh`: private machine-specific environment variables,
  such as API keys.
- `keys/`: a directory containing the SSH keys used by the machine.

### Packages

- `nvim`
- `oh-my-zsh`
- `pure` shell theme
- `bat`
- `eza`

### Git

- `~/.ssh/github.pub`: public key for GitHub.

## macOS Backup

- Raycast configuration
