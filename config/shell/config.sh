# Configuration (shared across machines)
# =============================================================================

COMPLETION_WAITING_DOTS="true" # show dots while loading completions
ENABLE_CORRECTION="true"       # enable command auto-correction
HYPHEN_INSENSITIVE="true"      # ignore hyphens in commands
ZSH_TMUX_AUTOSTART="true"      # start tmux automatically
ZSH_THEME=""                   # use external theme
zstyle ':omz:update' mode auto # update automatically without asking

plugins+=(
	git               # git aliases
	colored-man-pages # colorize man pages
	tmux              # tmux integration
)
# load oh-my-zsh
source $ZSH/oh-my-zsh.sh

# Shell Configuration
# =============================================================================

unsetopt auto_list   # don't echo choices on ambiguous completion
setopt menu_complete # auto-complete with menu selection

# auto-completion
zstyle ':completion:*' completer _expand _complete _correct _approximate
zstyle ':completion:*' format '%BCompleting %d:%b'
zstyle ':completion:*' group-name ''

# completions colors
zstyle ':completion:*:options' list-colors '=(#b)(*)-- *==34' '=^(-- *)=34'
zstyle ':completion:*:parameters' list-colors '=*=34'
zstyle ':completion:*:commands' list-colors '=*=1;32'
zstyle ':completion:*:builtins' list-colors '=*=1;32'
zstyle ':completion:*:functions' list-colors '=*=1;35'
zstyle ':completion:*:aliases' list-colors '=*=1;35'
zstyle ':completion:*:systemctl:*' list-colors '=(#b)*(-- *)==34' '=-- *=34'

# completion format of processes
zstyle ':completion:*:*:*:*:processes' command \
	"ps -u $USERNAME -o pid,%cpu,%mem,cputime,command"
zstyle ':completion:*:*:kill:*:processes' list-colors \
	'=(#b) #([0-9]#) #*[0-9]#:[0-9]#[:.][0-9]# #(*)=34=1;31=32'

# pure prompt
PURE_PROMPT_SYMBOL='➜'
autoload -U promptinit
promptinit
prompt pure

# Functions and Aliases
# =============================================================================

alias zreset='exec "$SHELL"'
alias cat='bat --paging=never'
alias ls='exa --group-directories-first --sort=Name --icons'
alias lst='ls -T'
alias lls='ls -lhmU --git --no-user'
alias llst='lls -T'

# time the startup of shell
ztime() {
	usage="usage: $0 [iterations]"
	if (($# > 1)); then echo $usage && return 1; fi
	for i in $(seq 1 ${1-1}); do time $SHELL -i -c exit; done
}
