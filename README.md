# Machine

This repository contains the configuration files and Python setup scripts for
various machines. It’s designed to streamline the setup and update process,
ensuring consistent configurations across all devices with minimal manual
intervention.

## Usage

To set up a machine, run the following command:
<!-- TODO - allow setting up different machines -->

```sh
url=https://raw.githubusercontent.com/mohdfareed/machine/main/bootstrap.py
curl -fsSL $url | python3 - [-f|--force] [-h|--help]
```

Where the arguments are as follows:

- `-f|--force`: forces cloning the repo even if it already exists.
- `-h|--help`: prints the help message.

### Setting Up Individual Components

Individual machine components can be set up by running the respective setup
module, provided that the bootstrapping script has already been run. Run the
following command to set up a component:

```sh
python -m scripts.[component] [-h]
```

### Updating and Cleaning

To update the machine, reapplying setup config, run the following command:

```sh
python -m [machine].setup [-h]
```

## Configuration

The common configuration that is shared across all machines. All machines must
have the configuration below.

### Files

- `$PRIVATE_MACHINE/env.sh`: private machine-specific environment variables,
  such as API keys.
- `keys/`: a directory containing the SSH keys used by the machine.

### Packages

- `oh-my-zsh`
- `pure`
- `nvim`
- `bat`
- `eza`

### Git

- `~/.ssh/github.pub`: public key for GitHub.

## macOS Backup

- Raycast configuration
