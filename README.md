# Machine

This repository contains the configuration files and Python setup scripts for
various machines. It’s designed to streamline the setup and update process,
ensuring consistent configurations across all devices with minimal manual
intervention.

## Usage

To set up a machine, run the following command:

```sh
repo_url='https://raw.githubusercontent.com/mohdfareed/machine/main'
script_url="${repo_url}/[machine]/bootstrap.py"
curl -fsSL $script_url | python3 - [-f|--force] [-v|--verbose] [-h|--help]
```

Where the arguments are as follows:

- `machine`: the machine to set up (only macOS is supported).
- `-f|--force`: forces cloning the repo even if it already exists.
- `-v|--verbose`: prints verbose output (debug messages).
- `-h|--help`: prints a help message.

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
- `dotnet-sdk`

### Git

- `~/.ssh/github.pub`: public key for GitHub.

## macOS Backup

- Raycast configuration
