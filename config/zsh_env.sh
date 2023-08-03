# Environment
# =============================================================================

# paths
export ZSHDIR="$MACHINE"
export ZSH="$HOME/.zsh/omz"

# config
export EDITOR="$(which micro)" # default to micro as the editor
export LESS="-R --ignore-case" # use less with colors
export SYSTEMD_LESS=$LESS      # less arguments of systemd pager
export BAT_PAGER="less $LESS"  # use less as the pager for bat
