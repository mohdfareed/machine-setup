#!/usr/bin/env sh

# variables
machine_path="$(dirname "$(realpath "$0")")"
script="$machine_path/bootstrap.py"
usage="Usage: bootstrap.sh ..."
error="\033[31;1mError:\033[0m Bootstrap script not found: $script"

# validation
if [ ! -f "$script" ]; then
    printf "$error\n"
    echo "$usage"
    exit 1
fi

# bootstrap
echo "Bootstrapping machine..."
$script "$@" || exit 1
