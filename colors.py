class color:
    """Color class for printing in color
    """

    reset = '\u001b[0m'
    bold = '\u001b[01m'
    underline = '\u001b[04m'
    reverse = '\u001b[07m'
    strikethrough = '\u001b[09m'

    class fg:
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

    class bg:
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

    def Bold(text): return color.bold + text + color.reset

    def Underline(text): return color.underline + text + color.reset

    def Reverse(text): return color.reverse + text + color.reset

    def Strikethrough(text): return color.strikethrough + text + color.reset

    def Red(text): return color.fg.red + text + color.reset

    def Green(text): return color.fg.green + text + color.reset

    def Yellow(text): return color.fg.yellow + text + color.reset

    def Blue(text): return color.fg.blue + text + color.reset

    def Magenta(text): return color.fg.magenta + text + color.reset

    def Cyan(text): return color.fg.cyan + text + color.reset

    def BrightRed(text): return color.fg.brightRed + text + color.reset

    def BrightGreen(text): return color.fg.brightGreen + text + color.reset

    def BrightYellow(text): return color.fg.brightYellow + text + color.reset

    def BrightBlue(text): return color.fg.brightBlue + text + color.reset

    def BrightMagenta(text): return color.fg.brightMagenta + text + color.reset

    def BrightCyan(text): return color.fg.brightCyan + text + color.reset
