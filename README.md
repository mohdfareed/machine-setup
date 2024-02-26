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

The repo expects the following files and directories to be present on the
machine:

- `$PRIVATE_MACHINE/env.sh`: private machine-specific environment variables,
  such as API keys and passwords.
- `$PRIVATE_MACHINE/pi.sh`: private Raspberry Pi-specific environment
  variables, equivalent to `env.sh`.
- `keys/`: a directory containing SSH keys used by the machine.
  - The current setup expects the following keys to be present:
    - `personal[.pub]`: key pair for personal GitHub account.

### Individual Setup

Individual machine components can be set up by running the respective setup
module, provided that the bootstrapping script has already been run. Run the
following command to set up a component:

```sh
python -m scripts.component [-h]
```

## Project Structure

The project has the following **hard-coded** structure:

- `config`: a module containing configuration files used by the machine. It
  defines references to all the configuration files in the repo. It must be
  updated whenever a new configuration file is added or its path modified.
- `raspberrypi`: a directory containing configuration files used by a Raspberry
  Pi.

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
