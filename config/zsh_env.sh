# Environment (shared across machines)
# =============================================================================

export ZSH="$HOME/.zsh/omz"    # oh-my-zsh path
export EDITOR="$(which micro)" # default to micro as the editor
export LESS="-R --ignore-case" # use less with colors
export SYSTEMD_LESS=$LESS      # less arguments of systemd pager
export BAT_PAGER="less $LESS"  # use less as the pager for bat

# Helper Functions
# =============================================================================

# update an environment variable, creating it if it doesn't exist
update_env() {
    usage="usage: $0 variable [value]"
    if [ $# -ne 1 ] && [ $# -ne 2 ]; then echo $usage && return 1; fi
    env=$(readlink -f $HOME/.zshenv)
    new_var="export $1=$2"
    pattern="^(export )?$1="

    # create it if it doesn't exist
    if ! grep -Eq $pattern $env; then
        echo $new_var >> $env
    else # if the variable exists, update it
        if [[ "$OSTYPE" == "darwin"* ]]; then # macOS
            sed -i '' -E "s/$pattern.*/$new_var/" $env
        else # GNU
            sed -i -r "s/$pattern.*/$new_var/" $env
        fi
    fi
    $new_var
}
