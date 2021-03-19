#!/usr/bin/env zsh

gem install colorls

# link colorls config if it is installed and let colorls point to it
which colorls > /dev/null
if [[ $? = 0 ]] ; then
    # link colorls configuration
    mkdir -p $XDG_CONFIG_HOME/colorls
    ln -siv $DOTFILES/other/dark_colors.yaml \
        $XDG_CONFIG_HOME/colorls/dark_colors.yaml

    # get path of file specifying config dir and update it
    colorls_path="$(dirname $(gem which colorls))/colorls/yaml.rb"
    sed -i '' 's#.config/colorls#Developer/colorls#' $colorls_path
fi
