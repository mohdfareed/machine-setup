# environment variables
$script = (Get-Item -Path $MyInvocation.MyCommand.Path).Target
if (-not $script) {
    $script = $MyInvocation.MyCommand.Path
}
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
if (-not (Get-Command -Name "oh-my-posh" -ErrorAction SilentlyContinue)) {
    $installScript = 'https://ohmyposh.dev/install.ps1'
    $webClient = New-Object System.Net.WebClient
    Set-ExecutionPolicy Bypass -Scope Process -Force
    Invoke-Expression ($webClient.DownloadString($installScript))
    Remove-Variable -Name "installScript"; Remove-Variable -Name "webClient"
}
$theme = "$env:POSH_THEMES_PATH/pure.omp.json"
oh-my-posh init pwsh --config "$theme" | Invoke-Expression
Remove-Variable -Name "theme"
