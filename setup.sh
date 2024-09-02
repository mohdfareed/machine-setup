#!/usr/bin/env zsh

usage="usage: $0 machine [args]"
machine=""
args=()

# parse arguments
for arg in "$@"; do
    if [ -z "$machine" ]; then
        machine="$arg"
    else
        args+=("$arg")
    fi
done

# check if setting up a github codespace
if [ -n "$CODESPACES" ]; then
    machine="codespaces"
fi

# ensure valid machine is provided
machine_path="$(dirname "$(realpath "$0")")"
if [ -z "$machine" ] || [ ! -d "$machine_path/machines/$machine" ]; then
    echo -e "\033[31;1mError:\033[0m Invalid machine name: '$machine'"
    echo "$usage"
    exit 1
fi

# setup =======================================================================

# set variables
venv_dir="$machine_dir/.venv"
req_file="$machine_dir/requirements.txt"
python="$venv_dir/bin/python"

# create virtual environment and install requirements
echo "Creating virtual environment..."
venv_options="--clear --upgrade-deps --prompt $machine"
python3 -m venv $venv_dir $venv_options > /dev/null 2>&1
$python -m pip install -r $req_file --upgrade > /dev/null 2>&1

# execute machine setup script
echo "Setting up machine '$machine'..."
cd "$machine_dir"
$python -m "machines.$machine.setup" "${args[@]}"
cd - >/dev/null
