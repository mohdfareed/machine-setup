#!/usr/bin/env sh

url="https://raw.githubusercontent.com/mohdfareed/machine/main/bootstrap.py"
curl -fsSL $url | python3 - "$@"
