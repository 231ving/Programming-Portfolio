"""Create player characters with different classes. Creates more generic
monsters as enemies.

Phuc Le
11/10/2023
Version 3.2
"""
from random import *
from item import *
from printer import *
from datetime import *


class CharacterDeathException(Exception):
    """Exception for when a player character is killed.
    """
    def __init__(self, msg: str, character: object) -> None:
        """Constructor for the exception instance.
        Args:
            msg (str): The string message to be printed.
            character (object): Specifically, the player character that died.
        Except:
            ValueError: The msg passed in wasn't a string or the character wasn't an object.
        """
        if isinstance(msg, str) and isinstance(character, Character):
            super().__init__(msg)
            self.character = character
        else:
            raise ValueError("The msg passed in must be a string and"
                             " the character passed in must be an object.")


class MonsterDeathException(Exception):
    """Exception for when a monster is killed."""
    def __init__(self, msg: str, monster: object) -> None:
        """Constructor for the exception instance.
        Args:
            msg (str): The string message to be printed.
            monster (object): Specifically, the monster that died.
        Except:
            ValueError: The msg passed in wasn't a string or the monster wasn't an object.
        """
        if isinstance(msg, str) and isinstance(monster, object):
            super().__init__(msg)
            self.monster = monster
        else:
            raise ValueError("The msg passed in must be a string and"
                             " the monster passed in must be an object.")


class CharacterOverweightException(Exception):
    """Exception for when a player character is carrying too much in their inventory.
    """
    def __init__(self, msg: str, character: object) -> None:
        """Constructor for the exception instance.
        Args:
            msg (str): The string message to be printed.
            character (object): Specifically, the player character that is overburdened.
        Except:
            ValueError: The msg passed in wasn't a string or the character wasn't an object.
        """
        if isinstance(msg, str) and isinstance(character, object):
            super().__init__(msg)
            self.character = character
        else:
            raise ValueError("The msg passed in must be a string and"
                             " the character passed in must be an object.")


class Character:
    """The base Character class containing from which the more specific
     player classes and Monster class is customized from.
    """
    def __init__(self, name: str) -> None:
        """The constructor for the Character instance.
        Args:
            name (str): The Character's name. Cannot be blank (Exception Handling)
        Except:
            ValueError: The character's name must be a non-empty string.
        """
        if isinstance(name, str) and name != "":
            self.__name = name
            self.__health = randint(50, 100)
            self.base_attack = randint(5, 20)
            self.base_defense = randint(5, 10)
            self.__base_luck = randint(1, 20)
            self.__inventory: list[Item] = []
            self.__armor: list[Armor] = []
            self.__weapon = Weapon(["weapon", "Barehanded", 0, 0, 0])
            self.__weapon.condition = ["Regular", 1.0]
            self.__inventory_weight = 0
            self.__max_weight = 5
        else:
            raise ValueError("The character's name must be a non-empty string.")

    @property
    def name(self) -> str:
        """Getter for the __name attribute:
        Returns:
            self.__name (str): The name of a character.
        """
        return self.__name

    def quick_info(self) -> str:
        """Returns a character's name and what class they are.
        Returns:
            str: The character's name and their specific class.
        """
        return self.__name + " the " + self.__class__.__name__

    @property
    def health(self) -> int:
        """Getter for the __health attribute.
        Returns:
            __health (int): The current health of a character.
        """
        return self.__health

    @health.setter
    def health(self, change: int) -> None:
        """Setter for the __health attribute.
        Args:
            change (int): The change to a character's current health amount.
            Defaults is increasing health.
        Except:
            CharacterDeathException: If the character's health hits or drops below 0.
        """
        try:
            self.__health = self.__health + change
            if self.health <= 0:
                raise CharacterDeathException("", self)
        except CharacterDeathException:
            print((self.quick_info() + "'s health is <=0."))

    @property
    def weapon(self) -> Weapon:
        """Getter for the __weapon attribute
        Returns:
            __weapon (Weapon): The weapon a character is wielding.
        """
        return self.__weapon

    @weapon.setter
    def weapon(self, weapon: Weapon) -> None:
        """Setter for the __weapon attribute.
        Args:
            weapon (Weapon): The new Weapon instance for the character to wield.
        Except:
            ValueError: The weapon argument must be a Weapon instance.
        """
        if isinstance(weapon, Weapon):
            self.__weapon = weapon
        else:
            raise ValueError("The weapon passed in must be a Weapon instance.")

    @property
    def armor(self) -> list[Armor]:
        """Getter for the armor a character is wearing.
        Returns:
            __armor (list[Armor]): The list of armor pieces a character is wearing.
        """
        return self.__armor

    @armor.setter
    def armor(self, armor_name: Armor) -> None:
        """Setter that modified the __armor attribute.
        Args:
            armor_name (Armor): The Armor instance the character will wear.
        Except:
            ValueError: The armor_name passed in is not an Armor instance.
        """
        if isinstance(armor_name, Armor):
            for armor in self.__armor:
                if armor.description == armor_name:
                    self.__armor.remove(armor_name)
                    self.__inventory.append(armor_name)
                self.__armor.append(armor_name)
        else:
            raise ValueError("The armor passed in wasn't an Armor instance.")

    def inventory(self) -> list[Item]:
        """Getter for the __inventory attribute.
        Returns:
            __inventory (list[Item]): The list of Items in a character's inventory.
        """
        return self.__inventory

    def in_inventory(self, item_description: str) -> Item | None:
        """Checks if the item is in the character's inventory or not.
        Args:
            item_description (str): The item description to search for.
        Returns:
            item (Item): The Item instance if it was found.
            None: If the Item instance wasn't found.
        Except:
            ValueError: The item_description wasn't a string.
        """
        if isinstance(item_description, str):
            for item in self.inventory():
                if isinstance(item, Item):
                    if item_description == item.description:
                        return item
                else:
                    return None
            return None
        else:
            raise ValueError("The item's description wasn't a string.")

    def add_inventory(self, item_name: Item) -> None:
        """Adds an Item instance to the character's inventory.
        Args:
            item_name (Item): The item to add to the inventory.
        Except:
            ValueError: The item_name passed in wasn't an Item instance.
        """
        if isinstance(item_name, Item):
            self.__inventory.append(item_name)
        else:
            raise ValueError("The item you wanted to add wasn't an Item instance.")

    def wearing(self, item_description: str) -> Armor | None:
        """Determines if the item_description inputted was already worn or not.
        Args:
            item_description (str): The item's description to look up.
        Returns:
            armor (Armor): The Armor instance if you were wearing the specified armor.
            None: If you weren't wearing the specified armor piece.
        Except:
            ValueError: The item_description passed in wasn't a string.
        """
        if isinstance(item_description, str):
            for armor in self.armor:
                if item_description == armor.description:
                    return armor
            return None
        else:
            raise ValueError("The item's description wasn't a string.")

    @property
    def base_attack(self) -> int:
        """Getter for the __base_attack attribute.
        Returns:
            __base_attack (int): A character's base attack.
        """
        return self.__base_attack

    @base_attack.setter
    def base_attack(self, attack: int) -> None:
        """Setter for the __base_attack attribute.
        Args:
            attack (int): What to set the character's base attack to.
        Except:
            ValueError: The attack passed in wasn't an integer, or it was
             outside the acceptable range of 0-30 inclusive.
        """
        if isinstance(attack, int) and (0 <= attack <= 30):
            self.__base_attack = attack
        else:
            raise ValueError("The attack passed in wasn't an integer, or it"
                             " was outside the acceptable range of 0-30 inclusive.")

    @property
    def base_defense(self) -> int:
        """Getter for the __base_defense attribute.
        Returns:
            __base_defense (int): A character's base defense.
        """
        return self.__base_defense

    @base_defense.setter
    def base_defense(self, defense: int) -> None:
        """Setter for the __base_defense attribute.
        Args:
            defense (int): What to set the character's base defense to.
        Except:
            ValueError: The defense passed in wasn't an integer, or it was
             outside the acceptable range of 0-20 inclusive.
        """
        if isinstance(defense, int):
            self.__base_defense = defense
        else:
            raise ValueError("The defense passed in wasn't an integer, or it"
                             " was outside the acceptable range of 0-20 inclusive.")

    @property
    def inventory_weight(self) -> int:
        """Calculates the weight of all items in a character's inventory
         and stores it as __inventory_weight.
        Returns:
            __inventory_weight (int): The weight a character is carrying.
        """
        self.__inventory_weight = 0
        for item in self.inventory():
            if isinstance(item, Item):
                self.__inventory_weight = self.__inventory_weight + item.weight
        return self.__inventory_weight

    @property
    def max_weight(self) -> int:
        """Getter for the __max_weight attribute.
        Returns:
            __max_weight (int): The maximum carry weight of a character.
        """
        return self.__max_weight

    def total_defense(self) -> int:
        """Calculates a character's total defense as a result of their
         base defense and all armor pieces worn.
        Returns:
            sum_defense (int): The total defense a character has.
        """
        sum_defense = self.__base_defense
        if not self.__armor:
            return sum_defense
        else:
            for armor in self.__armor:
                sum_defense = sum_defense + armor.added_defense
            return sum_defense

    def total_attack(self) -> int:
        """Calculates a character's total attack as a result of their
         base attack and the weapon they're wielding.
        Returns:
            sum_attack (int): The total attack a character has.
        """
        sum_attack = self.__base_attack + int(self.__weapon.added_attack)
        return sum_attack

    def take_damage(self, enemy: object) -> int:
        """Calculates the damage this character will take when attacked
         by the specified enemy.
        Args:
            enemy (object): Specifically, the Character instance that is attacking.
        Returns:
            damage (int): The damage this character will take expressed as a positive value.
        Except:
            ValueError: The enemy object passed in wasn't a Character instance.
        """
        if isinstance(enemy, Character):
            luck_dif = enemy.__base_luck - self.__base_luck
            damage = enemy.total_attack() - self.total_defense()
            if luck_dif > 0:
                if randint(0, 100) < luck_dif:
                    damage = 2 * enemy.total_attack()
                    print("Critical Hit! " + enemy.name + "'s attack ignored " + self.name + "'s defense.")
            if damage <= 0:
                return 0
            else:
                self.health = -damage
            return damage
        else:
            raise ValueError("The enemy object specified wasn't a Character instance.")

    def __str__(self) -> str:
        """String method containing all the information on a character.
        Returns:
            str: A long strong about a character's
             name, class, weapon, armor, inventory, and total stats.
        """
        self.__char_att = self.total_attack()
        self.__char_def = self.total_defense()
        self.__char_inv = []
        for item in self.inventory():
            if isinstance(item, Item):
                self.__char_inv.append(item.description)
        self.__armor_list = []
        for armor in self.armor:
            self.__armor_list.append(armor.description)

        return (self.quick_info() + " is wielding a " + self.weapon.description +
                " weapon and is wearing " + str(self.__armor_list) + ". They are carrying "
                + str(self.__char_inv) + ".\n Their stats are " + str(self.health)
                + " Health, " + str(self.__char_att) + " Attack, " + str(self.__char_def)
                + " Defense, and " + str(self.__base_luck) + " Luck.")


class Tank(Character):
    """A more specific role for a character, granting them additional defense.
    Inherits from the Character class.
    """
    def __init__(self, name: str) -> None:
        """Constructor for the Tank instance.
        Except:
            ValueError: The name passed in wasn't a string.
        """
        if isinstance(name, str):
            super().__init__(name)
            self.base_defense = int(self.base_defense * 1.2)
        else:
            raise ValueError("The name passed in wasn't a string.")


class DPT(Character):
    """A more specific role for a character, granting them additional attack.
    Inherits from the Character class.
    """
    def __init__(self, name: str) -> None:
        """Constructor for the DPT instance.
        Except:
            ValueError: The name passed in wasn't a string.
        """
        if isinstance(name, str):
            super().__init__(name)
            self.base_attack = int(self.base_attack * 1.2)
        else:
            raise ValueError("The name passed in wasn't a string.")


class Priest(Character):
    """A more specific role for a character, granting them healing abilities,
     preventing them from attacking, and protecting them from being attacked.
      Inherits from the Character class.
    """
    def __init__(self, name: str) -> None:
        """Constructor for the Priest instance.
        Except:
            ValueError: The name passed in wasn't a string.
        """
        if isinstance(name, str):
            super().__init__(name)
            self.last_healing = datetime.now() - timedelta(minutes=2)
        else:
            raise ValueError("The name passed in wasn't a string.")

    def take_damage(self, enemy: Character) -> int:
        """Calculates the damage this character will take when attacked
         by the specified enemy.
        Args:
            enemy (Character): The Character instance that is attacking you.
        Returns:
            int: The Priest can't be damaged by enemy attacks.
        Except:
            ValueError: The enemy passed in wasn't a Character instance.
        """
        if isinstance(enemy, Character):
            Printer.info(enemy.name + " senses the holiness of " + self.name +
                         " and chooses not to attack!")
            return 0
        else:
            raise ValueError("The enemy passed in wasn't a Character instance.")

    def heal(self, target: Character) -> int | None:
        """Heals the specified target for 0-25 health.
        Args:
           target (Character): The Character instance to be healed.
        Returns:
            None: If the Priest's healing ability is still on cooldown.
            amt (int): The amount the target will be healed for,
             a random integer between 0-25 inclusive.
        Except:
            ValueError: The target specified wasn't a Character instance.
        """
        if isinstance(target, Character):
            if datetime.now() - self.last_healing < timedelta(minutes=2):
                Printer.alert(self.name + " hasn't recovered from the last healing!")
                return None
            self.last_healing = datetime.now()
            amt = random.randint(0, 25)
            target.health = amt
            return amt
        else:
            raise ValueError("The target specified wasn't a Character instance.")


class Bard(Character):
    """A more specific role for a character, granting them weak healing abilities
     at the cost of reducing their own health. Inherits from the Character class.
    """
    def __init__(self, name: str) -> None:
        """Constructor for the Bard instance.
        Except:
            ValueError: The name passed in wasn't a string.
        """
        if isinstance(name, str):
            super().__init__(name)
            self.last_healing = datetime.now() - timedelta(minutes=0.25)
            self.health = -int(self.health * .20)
        else:
            raise ValueError("The name passed in wasn't a string.")

    def heal(self, target: Character) -> int | None:
        """Heals the specified target for 1-10 health.
        Args:
           target (Character): The Character instance to be healed.
        Returns:
            None: If the Bard's healing ability is still on cooldown.
            amt (int): The amount the target will be healed for,
             a random integer between 1-10 inclusive.
        Except:
            ValueError: The target specified wasn't a Character instance.
        """
        if isinstance(target, Character):
            if datetime.now() - self.last_healing < timedelta(minutes=0.25):
                Printer.alert(self.name + " hasn't recovered from the last healing!")
                return None
            self.last_healing = datetime.now()
            amt = random.randint(1, 10)
            target.health = amt
            Printer.info("  " + self.name + " sung the healing song!  ")
            print("  ~Tylenol, Advil, Morphine~  ")
            print("  ~Fight, Fight, Gold, Gold~  ")
            return amt
        else:
            raise ValueError("The target specified wasn't a Character instance.")


class Monster(Character):
    """The monster's to be fought, their stats depend on the default values
     specified in Character. Inherits from the Character class.
    """
    def __init__(self, name: str) -> None:
        """Constructor for the Monster instance.
        Except:
            ValueError: The name passed in wasn't a string.
        """
        if isinstance(name, str):
            super().__init__(name)
            self.health = -int(self.health // 2)  # Turned in -int(self.health - 1)
            self.base_attack = int(self.base_attack * 0.25)  # Turned in int(self.base_attack * 0.1)
            self.__base_luck = randint(1, 10)
            self.__gold = randint(0, 10)
            Item.load_items()
            Item.load_conditions()
            if randint(1, 10) == 1:  # Turned in randint(1, 10) >= 1
                item = random.choice(Item.ITEMS)
                if "weapon" == item[0]:
                    self.add_inventory(Weapon(item))
                else:
                    self.add_inventory(Armor(item))
        else:
            raise ValueError("The name passed in wasn't a string.")

    def __str__(self) -> str:
        """String method that returns a monster's information.
        Returns:
            str: A string containing a monster's name, stats,
             the gold they have, and the item they're carrying.
        """

        self.__mon_inv = []
        if self.inventory():
            self.__mon_inv = self.inventory()[0]
            return (self.name + " "
                    + str(self.health) + " Health, " + str(self.total_attack())
                    + " Attack, " + str(self.total_defense()) + " Defense, and "
                    + str(self.__base_luck) + " Luck.\n It is carrying " +
                    str(self.__gold) + " gold and an item of " +
                    str(self.__mon_inv.description) + ".")
        return (self.name + " "
                + str(self.health) + " Health, " + str(self.total_attack())
                + " Attack, " + str(self.total_defense()) + " Defense, and "
                + str(self.__base_luck) + " Luck.\n It is carrying " +
                str(self.__gold) + " gold.")

    @property
    def gold(self) -> int:
        """Getter for the __gold attribute.
        Returns:
            __gold (int): The gold coins a monster is carrying.
        """
        return self.__gold
