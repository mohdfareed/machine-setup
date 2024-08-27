#!/usr/bin/env bash

usage="usage: $0 machine [args]"

# initialize variables
machine=""
args=()

# github codespaces automatically executes the script with no arguments
if [ "$#" -eq 0 ]; then
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

# set python path
machine_dir="$(dirname "$(realpath "$0")")"
python="$machine_dir/.venv/bin/python"

# ensure machine exists
if [ ! -d "$machine_dir/machines/$machine" ]; then
    echo -e "\033[31;1mError:\033[0m Machine '$machine' does not exist"
    echo "$usage"
    exit 1
fi

# execute machine setup script
cd "$machine_dir"
$python -m "machines.$machine.setup" "${args[@]}"
cd - >/dev/null
