"""Allows for the printing of text in different colors.

Phuc Le
11/9/2023
Version 1.0
"""
from colorama import Back, Fore, Style


class Printer:
    """Contains various static methods for printing text.
    """
    @staticmethod
    def info(message) -> None:
        """Prints white text on a black background.
        General Use method.
        """
        print(Back.BLACK + Fore.LIGHTWHITE_EX + message.__str__())

    @staticmethod
    def alert(message) -> None:
        """Prints light red text on a black background.
        Used for drawing attention towards something.
        """
        print(Back.BLACK + Fore.LIGHTRED_EX + message.__str__())

    @staticmethod
    def dialogue(message) -> None:
        """Prints black text on a green background.
        Used when dialogue occurs.
        """
        print(Fore.BLACK + Back.LIGHTGREEN_EX + '"' + message.__str__() + '"')

    @staticmethod
    def text(message) -> None:
        """Prints white text on a black background.
        General use method.
        """
        print(Back.BLACK + Fore.LIGHTWHITE_EX + message.__str__())
