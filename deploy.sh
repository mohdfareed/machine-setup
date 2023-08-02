# Deploy a new machine. This will install Xcode Commandline Tools, accept the
# Xcode license, clone machine-setup, and execute the setup script.
# The machine path is hardcoded in the configuration files at: ~/machine/config
# Usage: ./deploy.sh <local_config_path>
# External effects:
#   - Accepts Xcode license
#   - Clones machine-setup to `~/Developer/machine`

# check usage
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <local_config_path>"
  exit 1
fi

# variables
local_config_path="$1"
repo=mohdfareed/machine.git
machine_dir=$HOME/Developer/machine

# check if xcode commandline tools are installed
if xcode-select --install &> /dev/null; then
    error='please install Xcode Commandline Tools and try again.'
    echo "\033[31;1mError:\033[0m $error"
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

# run setup script
cd $machine_dir && ./setup.py "$local_config_path"
