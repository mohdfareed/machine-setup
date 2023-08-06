# Environment (shared across machines)
# =============================================================================

# paths
export MACHINE="$(dirname $(realpath $0))" # machine path
export ZSH="$HOME/.zsh/omz"                # oh-my-zsh path

# config
export EDITOR="$(which micro)" # default to micro as the editor
export LESS="-R --ignore-case" # use less with colors
export SYSTEMD_LESS=$LESS      # less arguments of systemd pager
export BAT_PAGER="less $LESS"  # use less as the pager for bat

# Helper Functions
# =============================================================================

# update an environment variable, creating it if it doesn't exist
function update-env {
    usage="usage: $0 variable value"
    if (($# != 2)); then echo $usage && return 1; fi
    if [ -z ${!1+x} ]; then
        echo "$1=$2" >> $HOME/.zshenv
    else
        sed -i '' "s/^$1=.*/$1=$2/" $HOME/.zshenv
    fi
    export $1=$2
}

# unset an environment variable
function delete-env {
    usage="usage: $0 variable"
    if (($# != 1)); then echo $usage && return 1; fi
    sed -i '' "/^$1=.*/d" $HOME/.zshenv
    unset $1
}
