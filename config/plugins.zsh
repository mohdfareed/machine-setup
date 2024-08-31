# region - Plugins
# =============================================================================
# examples: https://zdharma-continuum.github.io/zinit/wiki/GALLERY

# extensions
zinit light zdharma-continuum/zinit-annex-unscope # reference without usernames
zinit light monitor # monitor for updates to file with url
zinit light patch-dl # download files with dl"URL file"

# # pure theme
# PURE_PROMPT_SYMBOL='➜' # prompt symbol
# PURE_PROMPT_VICMD_SYMBOL='»' # vi mode symbol
# PURE_CMD_MAX_EXEC_TIME=1 # show time if command takes more than 1 second
# zstyle :prompt:pure:git:stash show yes # show stash count
# zstyle :prompt:pure:git:fetch only_upstream yes # only show upstream changes
# zinit ice pick'async.zsh' src'pure.zsh'
# zinit light sindresorhus/pure

# oh-my-posh theme
if [[ ! $(command -v oh-my-posh) ]]; then
    curl -s https://ohmyposh.dev/install.sh | bash -s
fi
theme="$POSH_THEMES_PATH/pure.omp.json"
eval "$(oh-my-posh init zsh --config "$theme")" && unset theme

# syntax highlighting
zinit ice wait lucid atinit"ZINIT[COMPINIT_OPTS]=-C; zpcompinit; zpcdreplay;"
zinit light fast-syntax-highlighting

# auto-completions
zinit ice wait lucid atload"!_zsh_autosuggest_start"
zinit light zsh-users/zsh-autosuggestions

# completions
zinit ice wait lucid blockf atpull'zinit creinstall -q .'
zinit light zsh-users/zsh-completions
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' \
'r:|[._-]=* r:|=* l:|=*' # case-insensitive completion, ignore dots and hyphens

# fzf (fuzzy finder) tab completion
zinit ice wait lucid
zinit light Aloxaf/fzf-tab
# source: https://github.com/Aloxaf/fzf-tab?tab=readme-ov-file#configure
zstyle ':completion:*:git-checkout:*' sort false
zstyle ':completion:*:descriptions' format '[%d]'
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'eza -1 --color=always $realpath'
zstyle ':fzf-tab:*' switch-group '<' '>'
zstyle ':fzf-tab:*' fzf-command ftb-tmux-popup

# endregion
# region - Tools
# =============================================================================

# fzf (fuzzy finder)
zinit ice wait lucid as"program" from"gh-r" mv"fzf* -> fzf" pick"fzf" \
      atload"eval \"\$(fzf --zsh)\"" # key bindings for fzf (ctrl-t, ctrl-r)
zinit light junegunn/fzf

# eza (enhanced ls)
zinit ice wait lucid from"gh-r" as"program" mv"eza* -> eza"
zinit light eza-community/eza

# bat pager (cat with syntax highlighting)
zinit ice wait lucid as"command" from"gh-r" mv"bat* -> bat" pick"bat/bat"
zinit light sharkdp/bat

# btop
zinit ice wait lucid as"program" from"gh-r" atpull"./install.sh && ./setuid.sh" pick"btop"
zinit light aristocratos/btop

# nvim (neovim)
zinit ice wait lucid as"command" from"gh-r" mv"nvim* -> nvim" pick"neovim/neovim"
zinit light neovim/neovim

# tmux
zinit ice wait lucid as"command" from"gh-r" mv"tmux* -> tmux" pick"tmux/tmux"
zinit light tmux/tmux

# tmux plugin manager
[ ! -d $XDG_CONFIG_HOME/tmux/plugins/tpm ] &&
git clone https://github.com/tmux-plugins/tpm $XDG_CONFIG_HOME/tmux/plugins/tpm

# nvim dependencies ===========================================================

# lazygit
zinit ice wait lucid as"program" from"gh-r" mv"lazygit* -> lazygit" pick"lazygit"
zinit light jesseduffield/lazygit

# ripgrep
zinit ice wait lucid as"program" from"gh-r" mv"ripgrep* -> rg" pick"rg"
zinit light BurntSushi/ripgrep

# fd
zinit ice wait lucid as"command" from"gh-r" mv"fd* -> fd" pick"fd/fd"
zinit light sharkdp/fd

# endregion
