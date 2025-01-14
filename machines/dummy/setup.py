"""Setup module containing a `setup` function for a dummy machine."""

import config
import utils
from machines import LOGGER


@utils.machine_setup
def setup() -> None:
    """Setup a dummy machine."""
    LOGGER.warning("Setting up dummy machine...")
    LOGGER.info("This is executed if no machine is specified.")


if __name__ == "__main__":
    utils.startup()
    config.report(None)
    setup()
