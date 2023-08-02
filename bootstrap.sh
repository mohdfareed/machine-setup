#!/usr/bin/env sh
# Deploy a new machine. This will install Xcode Commandline Tools, accept the
# Xcode license, clone machine, and execute the setup script.

# Requirements: Xcode Commandline Tools
# Usage: ./deploy.sh local_config_path
#  - local_config_path: path to local config file, which contains two files:
#    - `machine.sh`: machine-specific environment, includes `MACHINE`
#    - `raspberrypi.sh`: raspberry pi environment, includes `MACHINE`

# External effects:
#   - Accepts Xcode license
#   - Clones machine to `~/Developer/machine`
#   - Creates a virtual environment at `~/Developer/machine/.venv`
#   - Executes `setup.sh` in machine

# check if valid machine path is provided
machine_env=$1/machine.sh
if [[ ! -f $machine_env ]]; then
    error="Machine file not found at: $machine_env"
    echo "\033[31;1m$error\033[0m"
    exit 1
fi
source "$machine_env"

# check if xcode commandline tools are installed
if xcode-select --install &> /dev/null; then
    error='Install Xcode Commandline Tools and try again.'
    echo "\033[31;1m$error\033[0m"
    exit 1
fi

# accept xcode license and load config
sudo --prompt 'Authenticate to accept Xcode license agreement: ' \
xcodebuild -license accept &> /dev/null

# prompt for cloning machine if it already exists
[[ -d $MACHINE ]] && \
echo "Machine directory already exists at: $MACHINE" && \
read -p "Do you want to overwrite it? (y|N) " answer && \
! [[ $answer =~ [Yy]|[Yy][e][s] ]] && clone=false || clone=true

# clone machine if prompted
if [[ $clone = true ]]; then
    echo "Cloning machine into '$MACHINE'..."
    rm -rf $MACHINE
    git clone -q https://github.com/mohdfareed/machine.git $MACHINE
fi

# setup virtual environment
echo "Setting up virtual environment..."
python venv $MACHINE/.venv
source $MACHINE/.venv/bin/activate &> /dev/null
pip install -q -r $MACHINE/requirements.txt &> /dev/null
# setup machine
cd $MACHINE && ./setup.py "$@"
