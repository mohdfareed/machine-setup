# environment variables
$script = (Get-Item -Path $MyInvocation.MyCommand.Path).Target -or $MyInvocation.MyCommand.Path
$env:MACHINE = Resolve-Path "$script/.."
Remove-Variable -Name "script"

# set execution policy
if ($IsWindows) {
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
}

# load homebrew in powershell
if (Test-Path -Path "/opt/homebrew/bin/brew") {
    $(/opt/homebrew/bin/brew shellenv) | Invoke-Expression
}

# oh-my-posh theme
if (Get-Command -Name "oh-my-posh" -ErrorAction SilentlyContinue) {
    $theme = "$env:POSH_THEMES_PATH/cert.omp.json"
    oh-my-posh init pwsh --config "$theme" | Invoke-Expression
    Remove-Variable -Name "theme"
}

<#
.SYNOPSIS
    Reloads the current PowerShell session.
#>
function Resolve-Profile {
    pwsh
}
