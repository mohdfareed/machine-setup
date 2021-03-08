# oh-my-zsh
export ZSH=~"/.oh-my-zsh"

# theme
ZSH_THEME="common"

# aliases
source $HOME/.aliases 

# default editor
export EDITOR=/usr/local/bin/code
export VISUAL=/usr/local/bin/code

# python
export PATH=/usr/local/opt/python/libexec/bin:$PATH

# rbenv
export RBENV_ROOT=/opt/homebrew/opt/rbenv
export PATH=$RBENV_ROOT/bin:$PATH
eval "$(rbenv init -)"

# plugins
plugins=(colored-man-pages)

# load oh-my-zsh
source $ZSH/oh-my-zsh.sh
# load colorls completion
source $(dirname $(gem which colorls))/tab_complete.sh
# load zsh autosuggestions
source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh
# load zsh syntax highlighting
source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh