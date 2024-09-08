# Machine

This repository contains the configuration files and Python setup scripts for
various machines. It’s designed to streamline the setup and update process,
ensuring consistent configurations across all devices with minimal manual
intervention.

## Requirements

- `python3`: the Python interpreter.
  - `pip`: the Python package manager.
  - `venv`: the Python virtual environment module.
- `git`: the version control system.
- `zsh`: if setting up a Unix machine.
- `powershell`: if setting up a Windows machine.

## Usage

To set up a machine, run the following command:

```sh
url="https://raw.githubusercontent.com/mohdfareed/machine/main/bootstrap.py"
curl -fsSL $url | python3 - [-h] [-f] [path] machine [-h]

# example:
# cd private_config_path (explained below)
# curl -fsSL $url | python3 - rpi
```

Or download it and run it locally:

```sh
./bootstrap.py [-h] [-f] [-p PATH] [machine] [-h] [-q] ...
```

Where the arguments are as follows:

- `-h|--help`: prints the bootstrapping help message.
- `-f|--force`: forces cloning the repo even if it already exists.
- `-p|--path`: the path to clone the repository into.
  - Defaults to `$MACHINE` then `$HOME/machine`.
- `machine`: the machine to set up, defaults to a testing machine.
- `-h|--help`: prints the machine's setup help message.
- `-q|--quiet`: suppresses debug output.
- `args`: the arguments required by the machine's setup script.

### Setting Up Individual Components

Individual machine components can be set up by running the respective setup
module, provided that the bootstrapping script has already been run. Run the
following command to set up a component:

```sh
python -m scripts.[component] [-h|--help]
```

Where the `args` are the arguments required by the component setup script.

### Updating and Cleaning

To update the machine and reapplying setup config, run the following command:

```sh
python -m machines.[machine].setup [-h|--help]
```

## Configuration

The `config` module contains common configuration that is shared across all
machines. It works without dependencies on machines modules.

The `scripts` module contains scripts that use the configuration to set up
individual components on the machine. Each script is designed to be run
independently of the machine setup script, failing on missing requirements.

A machine is configured by creating a new module in the `machines` package that
calls the appropriate scripts to set up the machine. The module can define
custom configuration files and scripts to be used by the setup script.


Machine modules have the following structure:

```plaintext
machines/
  [machine]/ # the machine's module, includes config files
    __init__.py # defines paths to config files
    setup.py # the machine's setup script
```

### Private Configuration

Some machines can have private configurations that cannot be shared publicly.
These configurations can be stored in a private directory and provided to the
machine's setup script as an argument, where supported.

The following are the private configuration files supported on all machines:

- `env.sh`: private environment variables, such as API keys; automatically
  sourced by `config.zshenv`.
- `keys/`: the SSH keys used by the machine; set up with `scripts.ssh`.

These files can be configured by calling
`config.load_private_config(config_path: str)` in the machine's setup script,
where `config_path` is the path to the private configuration directory
containing the files, read from the command line arguments.

## Machines

The following are notes related to specific supported machines.

### macOS

- `xcode-select --install` must be run before running the setup script.

Back up the following:

- Raycast configuration
- Downloads folder

### Raspberry Pi

- `zsh` must be installed before running the setup script.

### Windows

- `powershell` must be installed before running the setup script.
