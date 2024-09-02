#!/usr/bin/env zsh

script_name="$(basename "$0")"
usage="usage: $script_name [-h] {macos,rpi,codespaces} ...

Set up a machine with the provided name.

positional arguments:
  {macos,rpi,codespaces}  the name of the machine to set up
  args                    additional machine setup arguments

options:
  -h, --help              show this help message and exit"
machine=""
args=()

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
        args+=("$arg")
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
echo "Creating virtual environment..."
venv_options=(--clear --upgrade-deps --prompt "$machine")
python3 -m venv "${venv_options[@]}" "$venv_dir" > /dev/null 2>&1
$python -m pip install -r $req_file --upgrade > /dev/null 2>&1

# execute machine setup script
echo "Setting up machine '$machine'..."
cd "$machine_path"
$python -m "machines.$machine.setup" "${args[@]}"
cd - >/dev/null
