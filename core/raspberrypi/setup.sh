# update and upgrade
sudo apt update && sudo apt full-upgrade -y
# install packages
sudo apt install git -y
sudo apt install zsh -y
sudo apt install bat -y
sudo apt install exa -y
sudo apt install zsh-syntax-highlighting -y
sudo apt install zsh-autosuggestions -y
sudo apt install spaceship -y

# python version manager
curl https://pyenv.run | bash
# python dependencies
sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y

# set zsh as the default shell
chsh -s /bin/zsh
