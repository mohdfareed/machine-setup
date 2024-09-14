#!/usr/bin/env pwsh

$url = "https://raw.githubusercontent.com/mohdfareed/machine/main/bootstrap.py"
Invoke-WebRequest -Uri $url -UseBasicParsing |
Select-Object -ExpandProperty Content | python3 - $args
