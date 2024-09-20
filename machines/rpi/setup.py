"""Setup module containing a `setup` function for setting up a RPi."""

__all__ = ["setup"]

import config
import scripts
import utils
from machines import rpi
from scripts import package_managers

PACKAGES = ["zsh", "git", "code", "npm", "docker-compose"]


@utils.machine_setup
def setup() -> None:
    """Setup Raspberry Pi on a new machine."""

    # package managers
    apt = package_managers.APT()
    snap = package_managers.SnapStore(apt)

    # setup shell
    scripts.shell.setup(apt, rpi.zshrc, rpi.zshenv)
    scripts.tools.install_nvim(snap)
    scripts.tools.install_btop(snap)
    scripts.tools.install_powershell(snap)

    # setup ssh
    scripts.ssh.generate_key_pair("personal")
    scripts.ssh.setup(rpi.ssh_config)
    scripts.ssh.setup_server(apt)

    # setup core machine
    scripts.git.setup(apt)
    scripts.vscode.setup(snap)
    scripts.vscode.setup_tunnels("rpi")
    scripts.tailscale.setup(None)
    scripts.tools.setup_fonts(apt)

    # setup dev tools
    scripts.setup_docker(None)
    scripts.setup_python(apt)
    scripts.setup_node(None)
    snap.install("go", classic=True)
    snap.install("dotnet-sdk", classic=True)

    # machine-specific setup
    utils.shell.run("sudo loginctl enable-linger $USER", throws=False)  # code server
    utils.shell.run("sudo chsh -s $(which zsh)", throws=False)  # change default shell
    utils.shell.run("sudo touch $HOME/.hushlogin", throws=False)  # remove login message
    utils.shell.run("sudo mkdir -p $HOME/.config", throws=False)  # create config directory


if __name__ == "__main__":
    utils.startup()
    config.report(None)
    setup()
