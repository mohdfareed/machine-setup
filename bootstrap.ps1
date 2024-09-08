#!/usr/bin/env pwsh

$machinePath = (Get-Item -Path $PSCommandPath).DirectoryName
& python "$machinePath/bootstrap.ps1" @args
