# notebook's directory
notebook=~"/Library/Mobile Documents/com~apple~CloudDocs/Notebook"

# set VSCode as the default editor
export EDITOR=/usr/local/bin/code
export VISUAL=/usr/local/bin/code

# zsh tab-completion system
autoload -Uz compinit && compinit
# case-insensitive matching only if there are no case-sensitive matches
zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}'

# un-versioned symlinks to homebrew's python
export PATH=/usr/local/opt/python/libexec/bin:$PATH
