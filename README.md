# Machine

This repository contains the configuration files and Python setup scripts for
various machines. It’s designed to streamline the setup and update process,
ensuring consistent configurations across all devices with minimal manual
intervention.

## Usage

To set up a machine, run the following command:

```sh
github_url='https://raw.githubusercontent.com/mohdfareed'
script_url="${github_url}/[machine]/main/bootstrap.py"
curl -fsSL $script_url | python3 - [-h|--help] machine [-f|--force] [-h|--help]
```

Where the arguments are as follows:

- `-h|--help`: prints the bootstrapping help message.
- `machine`: the machine to set up (only macOS is supported).
- `-f|--force`: forces cloning the repo even if it already exists.
- `-h|--help`: prints the help message of the machine's setup script.

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

The common configuration that is shared across all machines. A machine is
configured by creating a new module in the `machines` package, with the
following structure:

```plaintext
machines/
  [machine]/
    config/
      zshenv.sh
    __init__.py
    setup.py
```

Where:

### Files

- `$PRIVATE_MACHINE/env.sh`: private machine-specific environment variables,
  such as API keys.
- `keys/`: a directory containing the SSH keys used by the machine.

### Shell

- `oh-my-zsh`
- `pure`
- `nvim`
- `bat`
- `eza`
- `dotnet-sdk`
- `zdotdir` defined in the machine's module.

### Git

- `~/.ssh/github.pub`: public key for GitHub.
- `xdg_config` defined in the machine's module.

## macOS Backup

- Raycast configuration
