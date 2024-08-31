#!/usr/bin/env zsh

usage="usage: $0 machine [args]"

# initialize arguments
machine=""
args=()

# check if setting up a codespace
if [ -n "$CODESPACES" ]; then
    machine="codespaces"
fi

# parse arguments
for arg in "$@"; do
    if [ -z "$machine" ]; then
        machine="$arg"
    else
        args+=("$arg")
    fi
done

# ensure machine is set
if [ -z "$machine" ]; then
    echo -e "\033[31;1mError:\033[0m Machine name is required"
    echo "$usage"
    exit 1
fi

# helpers =====================================================================

# Function to run commands silently
run() {
    silent=false
    for arg in "$@"; do
        if [ "$arg" = "-s" ] || [ "$arg" = "--silent" ]; then
            silent=true
            break
        fi
    done

    if [ "$silent" = true ]; then
        "$1" > /dev/null 2>&1
    else
        "$1"
    fi
}

# setup =======================================================================

# set variables
machine_dir="$(dirname "$(realpath "$0")")"
venv_dir="$machine_dir/.venv"
req_file="$machine_dir/requirements.txt"
python="$venv_dir/bin/python"

# create virtual environment and install requirements
echo "Creating virtual environment..."
venv_options="--clear --upgrade-deps --prompt $machine"
python3 -m venv $venv_dir $venv_options > /dev/null 2>&1
$python -m pip install -r $req_file --upgrade > /dev/null 2>&1

# ensure machine exists
if [ ! -d "$machine_dir/machines/$machine" ]; then
    echo -e "\033[31;1mError:\033[0m Machine '$machine' does not exist"
    echo "$usage"
    exit 1
fi

# execute machine setup script
echo "Setting up machine '$machine'..."
cd "$machine_dir"
$python -m "machines.$machine.setup" "${args[@]}"
cd - >/dev/null
