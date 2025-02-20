"""Stores information about the various weapons and armors that characters
 can wear/equip in the non-abstract Weapon and Armor classes.

Phuc Le
11/9/2023
Version 3.0
"""


import abc
import csv
import random
from typing import List


class Item(abc.ABC):
    """ABC that contains information about an abstract item.
    Attributes:
        CONDITIONS (List[List[str]]): The list containing all the potential
         conditions an item can have.
        ITEMS (List[List[str]]): The list containing all the potential item types.
    """
    CONDITIONS: List[List[str]] = []
    ITEMS: List[List[str]] = []

    @staticmethod
    def load_conditions() -> None:
        """Static method to load the different conditions an item can be in from a specified file.
        """
        with open('./item_attributes', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                Item.CONDITIONS.append(row)

    @staticmethod
    def load_items() -> None:
        """Static method to load the different types of items from a specified file.
        """
        with open('./item_types', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                Item.ITEMS.append(row)

    def __init__(self, attributes: list) -> None:
        """The constructor for the Item instance.
            Args:
                attributes (list): The list of attributes an item has.
            Except:
                ValueError: If the attributes passed to this instance are not
                 in a list of length 5+.
            """
        if isinstance(attributes, list) and len(attributes) >= 5:
            self.__attributes = attributes
            self.__name = attributes[1]
            self.__weight = int(attributes[4])

            Item.load_conditions()
            condition = random.choice(Item.CONDITIONS)
            self.condition = condition
        else:
            raise ValueError("The attributes passed to the Armor instance must be"
                             " in a list of at least length 5.")

    @property
    def name(self) -> str:
        """Getter for the __name attribute.
        Returns:
            __name (str): The item's name.
        """
        return self.__name

    @property
    def description(self) -> str:
        """Method that returns a short description of an item.
        Returns:
            str: A short string of an item's condition and name.
        """
        return self.__condition[0] + " " + self.__name

    @property
    def condition(self) -> list:
        """Getter for the __condition attribute.
        Returns:
            __condition (list): A list about the condition of an item.
        """
        return self.__condition

    @condition.setter
    def condition(self, _condition: list) -> None:
        """Setter for the __condition attribute.
        Args:
            _condition (list): An item's condition as a list with types [str, float].
        Except:
            ValueError: If the condition passed in weren't in the form of a
             list of length 2+ with types [str, float].
        """
        if isinstance(_condition, list) and len(_condition) >= 2:
            self.__condition = _condition
        else:
            raise ValueError("The item's conditions weren't in the form of a"
                             " list of length 2+ with types [str, float].")

    @property
    def weight(self) -> int:
        """Getter for the __weight attribute.
        Returns:
            __weight (int): The weight of an item as an integer.
        """
        return self.__weight

    @property
    def attributes(self) -> list:
        """Getter for the __attributes attribute.
        Returns:
            __attributes (list): The list of attributes an item's contain.
        """
        return self.__attributes


class Armor(Item):
    """Stores information about an armor piece. Inherits from the Item class.
    """
    def __init__(self, attributes) -> None:
        """The constructor for the Armor instance.
        Args:
            attributes (list): The list of attributes an armor piece has.
        Except:
            ValueError: If the attributes passed to this instance are not in a list of length 5+.
        """
        if isinstance(attributes, list) and len(attributes) >= 5:
            super().__init__(attributes)
            self.added_defense = self.attributes
            self.__armor_type = attributes[1]
        else:
            raise ValueError("The attributes passed to the Armor instance must be"
                             " in a list of at least length 5.")

    @property
    def added_defense(self) -> int:
        """Getter for the added_defense attribute.
        Returns:
            __added_defense (int): The defense increase provided by an armor piece.
        """
        return self.__added_defense

    @added_defense.setter
    def added_defense(self, attributes: list) -> None:
        """Setter for the defense an armor piece adds.
        Args:
            attributes (list): The list of attributes this armor piece has.
        Except:
            ValueError: If the armor's attributes aren't given as a list of
             length 5+ with types of [str, str, int, int, int].
        """
        try:
            if isinstance(attributes, list) and len(attributes) >= 5:
                self.__added_defense = round(float(attributes[3]) * float(self.condition[1]))
            else:
                raise ValueError
        except ValueError:
            print("The armor's attributes should be in a list with length at"
                  " least 5 with types of [str, str, int, int, int].")

    @property
    def type(self) -> str:
        """Getter for the type attribute.
        Returns:
            __armor_type (str): The type of armor.
        """
        return self.__armor_type


class Weapon(Item):
    """Stores information about a weapon. Inherits from the Item class.
    """
    def __init__(self, attributes: list) -> None:
        """The constructor for the Weapon class.
        Args:
            attributes (list): The list of attributes a weapon has.
        Except:
            ValueError: If the attributes passed to this instance are not in a list of length 5+.
        """
        if isinstance(attributes, list) and len(attributes) >= 5:
            super().__init__(attributes)
            self.added_attack = self.attributes
        else:
            raise ValueError("The attributes passed to the Weapon instance must be"
                             " in a list of at least length 5.")

    @property
    def added_attack(self) -> int:
        """Getter for the added_attack attribute.
        Returns:
            __added_attack (int): The attack increase provided by a weapon.
        """
        return self.__added_attack

    @added_attack.setter
    def added_attack(self, attributes: list) -> None:
        """Setter for the attack a weapon adds.
        Args:
            attributes (list): The list of attributes this weapon has.
        Except:
            ValueError: If the weapon's attributes aren't given as a list of
             length 5+ with types of [str, str, int, int, int].
        """
        try:
            if isinstance(attributes, list) and len(attributes) >= 5:
                self.__added_attack = round(float(attributes[2]) * float(self.condition[1]))
            else:
                raise ValueError
        except ValueError:
            print("The weapon's attributes should be in a list with length at least"
                  " 5 with types of [str, str, int, int, int].")
