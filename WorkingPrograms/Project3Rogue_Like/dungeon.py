"""Creates the dungeon room.

Phuc Le
11/9/2023
Version 3.0
"""
from random import *
from character import *


class Dungeon:
    """Contains information about the dungeon room itself and how the rooms
     are connected to one another.
    """
    def __init__(self, name: str, description: str) -> None:
        """Constructor Method for the Dungeon instance.
        Args:
            name (str): The room's name.
            description (str): The room's description
        Except:
            ValueError: The dungeon's name must be a non-empty string.
            ValueError: The dungeon's description must be a non-empty string.
        """
        if isinstance(name, str) and name != "":
            self.__name = name
        else:
            raise ValueError("The dungeon's name must be a non-empty string.")

        if isinstance(description, str) and description != "":
            self.__description = description
        else:
            raise ValueError("The dungeon's description must be a non-empty string.")

        self.__items: list[Item] = []
        self.__monsters: list[Monster] = []
        self.__prior = None
        self.__next = None
        self.__num_monsters = 0

        self.__monster_list = []
        with open("./monster_names") as f:
            self.__monster_list = f.readlines()

    def generate(self) -> None:
        """Generates the Dungeon and fills it with a random number
         of enemies from 0-4 inclusive.
        """
        self.__num_monsters = randint(0, 4)
        for num in range(0, self.__num_monsters):
            monster_name = random.choice(self.__monster_list)
            if not (self.monster_in_dungeon(monster_name) in self.__monsters):
                self.__monsters.append(Monster(monster_name))

    def monster_in_dungeon(self, mon_name: str | Monster) -> Monster | None:
        """Checks if the monster with the specified name is already in the dungeon.
        Args:
            mon_name (str | Monster): Either a string containing the monster's name
             or the Monster instance itself.
        Except:
            ValueError: If the mon_name isn't a string and isn't a Monster type.
        """
        if isinstance(mon_name, str) is False and isinstance(mon_name, Monster) is False:
            raise ValueError("mon_name must be of the Monster type or string type.")

        for monster in self.monsters:
            if f'{mon_name}\n' == monster.name or mon_name == monster.name:
                return monster
        return None

    def __str__(self) -> str:
        """String Method that gives the dungeon name, its description, and any items it has.
        Returns:
            __room_str (str): The string containing the dungeon's name, its description,
             and the list of items it has.
        """
        self.__room_inv = []
        for item in self.__items:
            self.__room_inv.append(item.description)
        self.__room_str = (str(self.__name) + ". " + str(self.__description) +
                           ". Items: " + str(self.__room_inv))
        return self.__room_str

    def __show_monsters__(self) -> str:
        """Returns a string if monsters are present in the room.
        Returns:
            str: If no monsters are present, 'No monsters (whew!)'.
            monster_str (str): Otherwise, a string containing the name
             of all monsters present in the room.
        """
        monster_str = "There is a "
        for monster in self.__monsters:
            monster_str = monster_str + str(monster.name) + " "
        monster_str = monster_str + "present in the room."
        if self.__monsters is []:
            return "No monsters (whew!)."
        return monster_str

    @property
    def monsters(self) -> list:
        """Getter for the __monsters attribute.
        Returns:
            __monsters (list): The list of Monster instances in the dungeon.
        """
        return self.__monsters

    @property
    def items(self) -> list:
        """Getter for the __items attribute.
        Returns:
            __items (list): The list of Item instances in the dungeon.
        """
        return self.__items

    @property
    def prior(self) -> type[object]:
        """Getter for the __prior attribute.
        Returns:
            __prior (type[object]): Specifically, the Dungeon instance prior to
             this one. The first room will have no prior Dungeon instance.
        """
        return self.__prior

    @prior.setter
    def prior(self, _prior: object) -> None:
        """Setter for the __prior attribute.
        Args:
            _prior (object): The Dungeon object that is designed to come before the current one.
        Except:
            ValueError: The prior dungeon is not a Dungeon object.
        """
        if isinstance(_prior, Dungeon):
            self.__prior = _prior
        else:
            raise ValueError("The prior dungeon is not a Dungeon object.")

    @property
    def next(self) -> type[object]:
        """Getter for the __next attribute.
        Returns:
            __next (type[object]): Specifically, the Dungeon instance next to
             this one.
        """
        return self.__next

    @next.setter
    def next(self, _next) -> None:
        """Setter for the __next attribute.
        Args:
            _next (object): The Dungeon object that is designed to come after the current one.
        Except:
            ValueError: The _next dungeon is not a Dungeon object.
        """
        if isinstance(_next, Dungeon):
            self.__next = _next
        else:
            raise ValueError("The _next dungeon is not a Dungeon object.")
