from .lib import display

def setup():
    display.header("Setting up Homebrew...")
    display.error("Homebrew error message.")
    display.warning("Homebrew warning message.")
    display.info("Homebrew information.")
    display.success("Homebrew success message.")
    display.output("Homebrew output message.")
    display.log("Homebrew log message.")
