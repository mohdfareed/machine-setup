#!/usr/bin/env pwsh

# Variables
$machinePath = (Get-Item -Path $PSCommandPath).DirectoryName
$script = "$machinePath/bootstrap.ps1"
$usage = "Usage: bootstrap.ps1 ..."
$error_msg = "`e[31;1mError:`e[0m Bootstrap script not found: $script"

# Validation
if (-not (Test-Path $script -PathType Leaf)) {
    Write-Error $error_msg
    Write-Error $usage
    exit 1
}

# Bootstrap
& python $script @args
