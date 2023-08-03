# Environment
# =============================================================================

# paths
export MACHINE="$(dirname $(realpath $0))" # machine path
export ZSH="$HOME/.zsh/omz"                # oh-my-zsh path

# config
export EDITOR="$(which micro)" # default to micro as the editor
export LESS="-R --ignore-case" # use less with colors
export SYSTEMD_LESS=$LESS      # less arguments of systemd pager
export BAT_PAGER="less $LESS"  # use less as the pager for bat
