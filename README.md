# Machine

This is a Python project that provides a collection of modules for
setting up various aspects of a machine, along with a library of utility
modules that are used throughout the project. The project also includes a
`setup.py` file that manages the setup process and is the entry point for the
project.

## Project Structure

The project has the following **hard-coded** structure:

- `config`: a directory containing configuration files used by the machine
- `raspberrypi`: a directory containing configuration files used by a Raspberry Pi

The setup scripts are in the following structure:

- `utils/`: a module of utilities used in by the setup scripts.
- `core/`: a collection of modules used to set up various aspects of the
machine, such as setting up Git, configuring Zsh and installing Homebrew.
- `setup.py`: the main setup script that is run to set up the machine.
- `deploy.sh`: a script that deploys the machine by setting up the repo and
running the setup script.
