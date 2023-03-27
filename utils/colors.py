"""Colors module that provides functions for formatting text using ANSI escape
sequences. The module also provides constants for the 16 ANSI colors and
decorations through the `Color`, `BackgroundColor` and `Decoration` classes.
"""

RESET = '\u001b[0m'
"""Reset all colors and decorations.
"""
LINE_UP = '\033[1A'
"""The ANSI escape sequence for moving the cursor up one line.
"""
LINE_CLEAR = '\x1b[2K'
"""The ANSI escape sequence for clearing the current line.
"""


class Color:
    """The 16 foreground ANSI color codes.
    """

    black = '\u001b[30m'
    red = '\u001b[31m'
    green = '\u001b[32m'
    yellow = '\u001b[33m'
    blue = '\u001b[34m'
    magenta = '\u001b[35m'
    cyan = '\u001b[36m'
    white = '\u001b[37m'
    bright_black = '\u001b[30;1m'
    bright_red = '\u001b[31;1m'
    bright_green = '\u001b[32;1m'
    bright_yellow = '\u001b[33;1m'
    bright_blue = '\u001b[34;1m'
    bright_magenta = '\u001b[35;1m'
    bright_cyan = '\u001b[36;1m'
    bright_white = '\u001b[37;1m'


class BackgroundColor:
    """The 16 background ANSI color codes.
    """

    black = '\u001b[40m'
    red = '\u001b[41m'
    green = '\u001b[42m'
    yellow = '\u001b[44m'
    blue = '\u001b[44m'
    magenta = '\u001b[45m'
    cyan = '\u001b[46m'
    white = '\u001b[47m'
    bright_black = '\u001b[40;1m'
    bright_red = '\u001b[41;1m'
    bright_green = '\u001b[42;1m'
    bright_yellow = '\u001b[44;1m'
    bright_blue = '\u001b[44;1m'
    bright_magenta = '\u001b[45;1m'
    bright_cyan = '\u001b[46;1m'
    bright_white = '\u001b[47;1m'


class Decoration:
    """ANSI decoration codes.
    """

    bold = '\u001b[01m'
    underline = '\u001b[04m'
    reversed = '\u001b[07m'
    strikethrough = '\u001b[09m'


def bold(text: str) -> str:
    """Sets the text to bold.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Decoration.bold + text + RESET


def underline(text: str) -> str:
    """Sets the text to underlined.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Decoration.underline + text + RESET


def reverse(text: str) -> str:
    """Reverses the foreground and background colors.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Decoration.reversed + text + RESET


def strikethrough(text: str) -> str:
    """Sets the text to strikethrough.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Decoration.strikethrough + text + RESET


def black(text: str) -> str:
    """Sets the text to black.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.black + text + RESET


def red(text: str) -> str:
    """Sets the text to red.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.red + text + RESET


def green(text: str) -> str:
    """Sets the text to green.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.green + text + RESET


def yellow(text: str) -> str:
    """Sets the text to yellow.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.yellow + text + RESET


def blue(text: str) -> str:
    """Sets the text to blue.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.blue + text + RESET


def magenta(text: str) -> str:
    """Sets the text to magenta.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.magenta + text + RESET


def cyan(text: str) -> str:
    """Sets the text to cyan.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.cyan + text + RESET


def bright_black(text: str) -> str:
    """Sets the text to bright black.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.bright_black + text + RESET


def bright_red(text: str) -> str:
    """Sets the text to bright red.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.bright_red + text + RESET


def bright_green(text: str) -> str:
    """Sets the text to bright green.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.bright_green + text + RESET


def bright_yellow(text: str) -> str:
    """Sets the text to bright yellow.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.bright_yellow + text + RESET


def bright_blue(text: str) -> str:
    """Sets the text to bright blue.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.bright_blue + text + RESET


def bright_magenta(text: str) -> str:
    """Sets the text to bright magenta.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.bright_magenta + text + RESET


def bright_cyan(text: str) -> str:
    """Sets the text to bright cyan.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return Color.bright_cyan + text + RESET


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
