reset = '\u001b[0m'


class Color:
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
    bold = '\u001b[01m'
    underline = '\u001b[04m'
    reversed = '\u001b[07m'
    strikethrough = '\u001b[09m'


def bold(text): return Decoration.bold + text + reset


def underline(text): return Decoration.underline + text + reset


def reverse(text): return Decoration.reversed + text + reset


def strikethrough(text): return Decoration.strikethrough + text + reset


def red(text): return Color.red + text + reset


def green(text): return Color.green + text + reset


def yellow(text): return Color.yellow + text + reset


def blue(text): return Color.blue + text + reset


def magenta(text): return Color.magenta + text + reset


def cyan(text): return Color.cyan + text + reset


def bright_red(text): return Color.bright_red + text + reset


def bright_green(text): return Color.bright_green + text + reset


def bright_yellow(text): return Color.bright_yellow + text + reset


def bright_blue(text): return Color.bright_blue + text + reset


def bright_magenta(text): return Color.bright_magenta + text + reset


def bright_cyan(text): return Color.bright_cyan + text + reset
