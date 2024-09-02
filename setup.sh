#!/usr/bin/env sh

script_name="$(basename "$0")"
usage="usage: $script_name [-h] machine ...

Set up a machine with the provided name.

positional arguments:
  machine     the name of the machine to set up
  args        additional machine setup arguments

options:
  -h, --help  show this help message and exit"
machine=""
args=""

# arguments ===================================================================

# check for help flag
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "$usage"
    exit 0
fi

# check if setting up a github codespace
if [ -n "$CODESPACES" ]; then
    machine="codespaces"
fi

# parse machine and its arguments
for arg in "$@"; do
    if [ -z "$machine" ]; then
        machine="$arg"
    else
        args="$args $arg"
    fi
done

# ensure valid machine is provided
machine_path="$(dirname "$(realpath "$0")")"
if [ -z "$machine" ] || [ ! -d "$machine_path/machines/$machine" ]; then
    echo -e "\033[31;1mError:\033[0m Invalid machine name: '$machine'"
    echo $usage
    exit 1
fi

# setup =======================================================================

# set variables
venv_dir="$machine_path/.venv"
req_file="$machine_path/requirements.txt"
python="$venv_dir/bin/python"

# create virtual environment and install requirements
if [ ! -d "$venv_dir" ]; then # only if it doesn't exist
    echo "Creating virtual environment..."
    python3 -m venv --clear --prompt "$machine" --upgrade-deps "$venv_dir"
    $python -m pip install -r $req_file --upgrade
fi

# execute machine setup script
echo "Setting up machine '$machine'..."
cd "$machine_path"
$python -m "machines.$machine.setup" $args
cd - > /dev/null
