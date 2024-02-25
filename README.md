# Machine

This is a Python project that provides a collection of modules for
setting up various aspects of a machine, along with a library of utility
modules that are used throughout the project.

## Usage

To set up the machine, run the following command:

```sh
url=https://raw.githubusercontent.com/mohdfareed/machine/main/bootstrap.py
curl -fsSL $url | python3 - [--force]
```

Where the arguments are as follows:

- `--force`: forces cloning the repo even if it already exists.
- `setup_args`: additional arguments to pass to the setup script.

The `config_dir` argument is the path to the directory containing the local
configuration files. This includes the following:

- `machine.sh`: private machine-specific data, such as API keys and passwords.
- `pi.sh`: private Raspberry Pi-specific data, equivalent to `machine.sh`.
- `keys/`: a directory containing SSH keys used by the machine.

### Individual Setup

Individual machine components can be set up by running the respective setup
module, provided that the bootstrapping script has already been run. Run the
following command to set up a component:

```sh
python -m core.component [-h]
```

## Project Structure

The project has the following **hard-coded** structure:

- `config`: a module containing configuration files used by the machine. It
  defines references to all the configuration files in the repo. It must be
  updated whenever a new configuration file is added or its path modified.
- `raspberrypi`: a directory containing configuration files used by a Raspberry
  Pi.

The setup scripts are in the following structure:

- `bootstrap.py`: a script that bootstraps a machine by setting up the repo and
  running the setup script.
- `setup.py`: the entrypoint script that is run to set up the machine.
- `core/`: a collection of modules used to set up various aspects of the
  machine, such as setting up Git, configuring shell and installing packages.
- `utils/`: a module of utilities used in by the setup scripts.

## Raspberry Pi

A locally-configured Raspberry Pi is configured by setting up the machine
directory on the Pi. The `raspberrypi` directory contains the configuration
files used by the Pi, which are copied to the machine directory on the Pi. The
script acts similarly to the `bootstrap.py` script, except that is adds the
setup entrypoint to the path without running it. To setup the Pi after running
this script, run:

```sh
setup-machine
```

The initial setup of the Raspberry Pi (done before running this script) is
done by installing **Raspberry Pi OS Lite (x64)** on an SD card and configuring
it as following:

- Enable SSH using password authentication.
- Set the username and password.
- Configure the wireless network, including setting the country to `US`.
