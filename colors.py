reset = '\u001b[0m'
bold = '\u001b[01m'
underline = '\u001b[04m'
reverse = '\u001b[07m'
strikethrough = '\u001b[09m'


class Color:
    black = '\u001b[30m'
    red = '\u001b[31m'
    green = '\u001b[32m'
    yellow = '\u001b[33m'
    blue = '\u001b[34m'
    magenta = '\u001b[35m'
    cyan = '\u001b[36m'
    white = '\u001b[37m'
    brightBlack = '\u001b[30;1m'
    brightRed = '\u001b[31;1m'
    brightGreen = '\u001b[32;1m'
    brightYellow = '\u001b[33;1m'
    brightBlue = '\u001b[34;1m'
    brightMagenta = '\u001b[35;1m'
    brightCyan = '\u001b[36;1m'
    brightWhite = '\u001b[37;1m'


class BG:
    black = '\u001b[40m'
    red = '\u001b[41m'
    green = '\u001b[42m'
    yellow = '\u001b[44m'
    blue = '\u001b[44m'
    magenta = '\u001b[45m'
    cyan = '\u001b[46m'
    white = '\u001b[47m'
    brightBlack = '\u001b[40;1m'
    brightRed = '\u001b[41;1m'
    brightGreen = '\u001b[42;1m'
    brightYellow = '\u001b[44;1m'
    brightBlue = '\u001b[44;1m'
    brightMagenta = '\u001b[45;1m'
    brightCyan = '\u001b[46;1m'
    brightWhite = '\u001b[47;1m'


def Bold(text): return bold + text + reset


def Underline(text): return underline + text + reset


def Reverse(text): return reverse + text + reset


def Strikethrough(text): return strikethrough + text + reset


def Red(text): return Color.red + text + reset


def Green(text): return Color.green + text + reset


def Yellow(text): return Color.yellow + text + reset


def Blue(text): return Color.blue + text + reset


def Magenta(text): return Color.magenta + text + reset


def Cyan(text): return Color.cyan + text + reset


def BrightRed(text): return Color.brightRed + text + reset


def BrightGreen(text): return Color.brightGreen + text + reset


def BrightYellow(text): return Color.brightYellow + text + reset


def BrightBlue(text): return Color.brightBlue + text + reset


def BrightMagenta(text): return Color.brightMagenta + text + reset


def BrightCyan(text): return Color.brightCyan + text + reset
