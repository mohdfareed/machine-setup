# Check for homebrew and install if needed
echo "Installing homebrew ..."

which -s brew
if [[ $? != 0 ]] ; then
  yes | /usr/bin/ruby -e "$(curl -fsSL \
    https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
  echo "Homebrew already installed ..."
fi

brew update

# UNIX shell (command interpreter)
brew install zsh
# Fish-like fast/unobtrusive autosuggestions for zsh
brew install zsh-autosuggestions
# Fish shell like syntax highlighting for zsh
brew install zsh-syntax-highlighting

# Distributed revision control system
brew install git
# Interpreted, interactive, object-oriented programming language
brew install python
# Ruby version manager
brew install rbenv

# Mac App Store command-line interface
brew install mas

# Open-source code editor
brew install --cask visual-studio-code
# Unpacks archive files
cask the-unarchiver
# Open-source BitTorrent client
brew install --cask transmission
# Free and open-source media player
brew install --cask iina

# App Store applications
mas install 441258766 # Magnet
mas install 409201541 # Pages
mas install 409203825 # Numbers
mas install 409183694 # Keynote
mas install 1320666476 # Wipr
mas install 1438243180 # Dark Reader
mas install 1505779553 # Dashlane

# fonts
brew tap homebrew/cask-fonts
brew install --cask font-hack-nerd-font
brew install --cask font-sf-pro
brew install --cask font-sf-compact
brew install --cask font-sf-mono
brew install --cask font-new-york

brew cleanup

# fix “zsh compinit: insecure directories”
# chmod -R go-w "$(brew --prefix)/share"
