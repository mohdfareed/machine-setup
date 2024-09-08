#!/usr/bin/env sh

# variables
machine_path="$(dirname "$(realpath "$0")")"
"$machine_path/bootstrap.py" "$@" || exit 1
