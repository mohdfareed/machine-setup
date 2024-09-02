#!/usr/bin/env pwsh

$scriptName = $(Split-Path -Leaf $PSCommandPath)
$usage = @"
Usage: $scriptName [-h] <machine> ...

Set up a machine with the provided name.

positional arguments:
  machine     the name of the machine to set up
  args        additional machine setup arguments

options:
  -h, --help  show this help message and exit
"@
$machine = ""
$machineArgs = @()

# Arguments ===================================================================

# Check for help flag
if ($args.Count -gt 0 -and ($args[0] -eq "--help" -or $args[0] -eq "-h")) {
    Write-Host $usage
    exit 0
}

# Parse machine and its arguments
foreach ($arg in $args) {
    if (-not $machine) {
        $machine = $arg
    }
    else {
        $machineArgs += $arg
    }
}

# Ensure a valid machine is provided
$machinePath = (Get-Item -Path $PSCommandPath).DirectoryName
if (-not $machine -or -not (Test-Path "$machinePath/machines/$machine")) {
    Write-Host "`e[31;1mError:`e[0m Invalid machine name: '$machine'"
    Write-Host $usage
    exit 1
}

# Setup =======================================================================

# Set variables
$venvDir = "$machinePath\.venv"
$reqFile = "$machinePath\requirements.txt"
$python = "$venvDir\Scripts\python.exe"

# Create virtual environment and install requirements
Write-Host "Creating virtual environment..."
$venvOptions = "--clear --upgrade-deps --prompt $machine"
python -m venv $venvOptions $venvDir > $null 2>&1
& $python -m pip install -r $reqFile --upgrade > $null 2>&1

# Execute machine setup script
Write-Host "Setting up machine '$machine'..."
Push-Location $machinePath
& $python -m "machines.$machine.setup" @machineArgs
Pop-Location > $null
