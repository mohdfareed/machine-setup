#!/usr/bin/env python3
from colors import Bold, BrightRed, BrightGreen


def main():
    info("Setting up Homebrew...")



def error(message): print(BrightRed(message))


def success(message): print(BrightGreen(message))


def info(message): print(Bold(message))


if __name__ == "__main__":
    main()
