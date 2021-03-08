#!/usr/bin/env zsh

echo "Installing latest version of Ruby..."

# get the latest version number of Ruby
version=$(rbenv install -l 2> /dev/null | grep -v '-' | tail -1)

# prompt the user for confirmation
while true; do
    echo "Ruby version $version will be installed."
    echo "Would you like to continue?[Y|n]"
    read answer

    case $answer in
        * )
            rbenv install $version; break;;
        [Nn]* )
            exit;;
    esac
done

# set default Ruby version
rbenv global $version
rbenv rehash

# install gems
echo "Installing gems..."
gem install bundler # applications' dependencies manager
gem install pry     # runtime developer console and IRB alternative
gem install byebug  # Ruby debugger
gem install rails   # full-stack web framework
gem install colorls # CLI gem that beautifies the terminal's ls command
