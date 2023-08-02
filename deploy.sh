#!/usr/bin/env sh
# Deploy a new machine. This will install Xcode Commandline Tools, accept the
# Xcode license, clone machine-setup, and execute the setup script.
# The machine path is hardcoded in the configuration files at: ~/machine/config
# Usage: ./deploy.sh [local_config_path]

# External effects:
#   - Accepts Xcode license
#   - Clones machine to `~/Developer/machine`
#   - Creates a virtual environment at `~/Developer/machine/.venv`
#   - Executes `setup.sh` in machine

# variables
repo=mohdfareed/machine.git
machine_dir=$HOME/Developer/machine

# check if xcode commandline tools are installed
if xcode-select --install &> /dev/null; then
    error='Install Xcode Commandline Tools and try again.'
    echo "\033[31;1m$error\033[0m"
    exit 1
fi

# accept xcode license
sudo --prompt 'Authenticate to accept Xcode license agreement: ' \
xcodebuild -license accept &> /dev/null

# prompt for cloning machine if it already exists
[[ -d $machine_dir ]] && \
echo "Machine directory already exists at: $(dirname $machine_dir)" && \
read -p "Do you want to overwrite it? (y|N) " answer && \
! [[ $answer =~ [Yy]|[Yy][e][s] ]] && clone=false || clone=true

# clone machine if prompted
if [[ $clone = true ]]; then
    echo "Cloning machine into '$machine_dir'..."
    rm -rf $machine_dir
    git clone -q https://github.com/$repo $machine_dir
fi

# setup virtual environment
echo "Setting up virtual environment..."
python venv $machine_dir/.venv &> /dev/null
source $machine_dir/.venv/bin/activate &> /dev/null
pip install -q -r $machine_dir/requirements.txt &> /dev/null
# setup machine
cd $machine_dir && ./setup.py "$@"
