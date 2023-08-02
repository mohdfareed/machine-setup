# Machine

This is a Python project that provides a collection of modules for
setting up various aspects of a machine, along with a library of utility
modules that are used throughout the project.

## Usage

To set up the machine, run the following command:

```bash
url=https://raw.githubusercontent.com/mohdfareed/machine/main/bootstrap.sh
curl -fsSL $url | python3 - path/to/machine/config_dir
```

The `config_dir` argument is the path to the directory containing the local
configuration files. This includes the following:

- `keys/`: a directory containing SSH keys used by the machine.
- `machine.sh`: a shell script that defines variable `MACHINE`, which is the
path to the machine repo. It also includes machine-specific data.
- `pi.sh`: equivalent to `machine.sh`, but is used to setup a Raspberry Pi.

## Project Structure

The project has the following **hard-coded** structure:

- `config`: a directory containing configuration files used by the machine
- `raspberrypi`: a directory containing configuration files used by a Raspberry
Pi.

The setup scripts are in the following structure:

- `utils/`: a module of utilities used in by the setup scripts.
- `core/`: a collection of modules used to set up various aspects of the
machine, such as setting up Git, configuring Zsh and installing Homebrew.
- `setup.py`: the main setup script that is run to set up the machine.
- `bootstrap.py`: a script that bootstraps a machine by setting up the repo and
running the setup script.
