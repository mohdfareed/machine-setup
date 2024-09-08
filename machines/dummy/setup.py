"""Setup module containing a `setup` function for a dummy machine."""

import config
import utils
from machines import LOGGER


def setup() -> None:
    """Setup a dummy machine."""
    LOGGER.warning("Setting up dummy machine for testing...")
    LOGGER.info("This machine is used if no machine is specified.")
    LOGGER.info("Dummy machine setup complete.")


if __name__ == "__main__":
    args = utils.startup(description="Dummy machine setup script.")
    config.report(None)
    utils.execute(setup)
