"""Setup module containing a `setup` function for setting up APT on a on a new
Debian machine."""

import logging

import utils

LOGGER = logging.getLogger(__name__)
"""The apt setup logger."""


def setup() -> None:
    """Setup apt on a new Debian machine."""
    if not is_installed():
        raise utils.UnsupportedOS("APT is not installed on this machine.")

    LOGGER.info("Setting up Debian apt...")
    utils.shell.run("sudo apt update && sudo apt upgrade -y")
    install("zsh git git-lfs gh")
    LOGGER.debug("Debian apt was setup successfully.")


def install(package: str) -> None:
    """Install an apt package."""
    LOGGER.info("Installing %s from apt...", package)
    utils.shell.run(f"sudo apt install -y {package}")
    utils.shell.run("sudo apt autoremove -y")
    LOGGER.debug("%s was installed successfully.", package)


def setup_snap() -> None:
    """Setup the snap store on a new Debian machine."""
    LOGGER.info("Setting up the snap store...")
    install("snapd")
    install_snap("snapd")
    LOGGER.debug("The snap store was setup successfully.")


def install_snap(package: str, classic=False) -> None:
    """Install a snap store package."""
    LOGGER.info("Installing %s from the snap store...", package)
    utils.shell.run(
        f"sudo snap install {package} {'--classic' if classic else ''}"
    )
    utils.shell.run("sudo snap refresh")
    LOGGER.debug("%s was installed successfully.", package)


def setup_docker(dev=False) -> None:
    """Setup docker on a new Debian machine."""
    LOGGER.info("Setting up Docker...")

    if dev:  # install with automated script for development
        utils.shell.run("curl -fsSL https://get.docker.com | sh")
        return

    # install with snap store
    install_snap("docker")
    utils.shell.run("sudo addgroup --system docker")
    utils.shell.run("sudo adduser $USER docker && newgrp docker")
    utils.shell.run("sudo snap enable docker")
    utils.shell.run("sudo apt install -y docker-compose")

    LOGGER.debug("Docker was setup successfully.")


def setup_python() -> None:
    """Setup python on a new Debian machine."""
    LOGGER.info("Setting up Python...")

    install("pip pipx")
    utils.shell.run("curl https://pyenv.run | bash")
    utils.shell.run(
        "git clone https://github.com/pyenv/pyenv-virtualenv.git "
        "$(pyenv root)/plugins/pyenv-virtualenv"
    )
    LOGGER.debug("Python was setup successfully.")


def setup_node() -> None:
    """Setup node on a new Debian machine."""
    LOGGER.info("Setting up Node...")

    install_snap("node", classic=True)
    url = "https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh"
    utils.shell.run(f"curl -o- {url} | bash")
    LOGGER.debug("Node was setup successfully.")


def is_installed() -> bool:
    """Check if apt is installed on the machine."""
    return utils.is_installed("apt")


def is_snap_installed() -> bool:
    """Check if the snap store is installed on the machine."""
    return utils.is_installed("snap")


if __name__ == "__main__":
    args = utils.startup(description="Snap store setup script.")
    utils.execute(setup, args.xdg_config)
