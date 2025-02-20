"""
A rogue-like text-based adventure game.

Phuc Le
11/10/2023a
Version 3.2
"""

import time
from typing import Optional, Dict, Callable

from colorama import Style
from character import *
from dungeon import *
from printer import *
import time


class Game:
    """The base Game itself, containing all the different commands.
    """
    def __init__(self) -> None:
        """Constructor for the Game instance.
        """
        # A list of the characters in the part
        self.__party: List[Character] = []
        # Current party gold
        self.__gold = 0
        # Starting dungeon
        self.__dungeons = [Dungeon("Dungeon Entrance",
                                   "The mouth of a giant cavern."
                                   " Danger lurks just past this door.")]
        # A reference to the current dungeon
        self.__current_location = self.__dungeons[0]
        # Add the commands
        self.__commands: Dict[str, Callable] = {}
        self.__setup_commands()
        # Start it up!
        self.__print_welcome()

    '''
    Adds the commands to the command dictionary.  This is a dictionary of strings keys that have
    function values.  This allows us to add/remove commands to the game easily by simply writing
    a new function and adding a dictionary key.
    '''
    def __setup_commands(self) -> None:
        """Adds the commands to the command dictionary. This is a dictionary
         of strings keys that have function values. This allows us to add/remove
          commands to the game easily by simply writing a new function and
           adding a dictionary key.
        """
        self.__commands["help"] = self.__show_help
        self.__commands["?"] = self.__show_help
        self.__commands["advance"] = self.__advance
        self.__commands["retreat"] = self.__retreat
        self.__commands["attack"] = self.__attack
        self.__commands["heal"] = self.__heal
        self.__commands["party"] = self.__party_stats
        self.__commands["stats"] = self.__stats
        self.__commands["gold"] = self.__see_gold
        self.__commands["take"] = self.__take
        self.__commands["inventory"] = self.__player_inventory
        self.__commands["equip"] = self.__equip
        self.__commands["wear"] = self.__wear
        self.__commands["remove"] = self.__remove
        self.__commands["drop"] = self.__drop
        self.__commands["monsters"] = self.__show_monsters
        self.__commands["leave"] = self.__leave_dungeons
        self.__commands["exit"] = self.__exit

    '''
    A priest can heal a single party member for between 0 and 25 health.
    '''
    def __heal(self, healer: Priest | Bard, player: str, *args) -> None:
        """Command to heal a designated player.
        Args:
            healer (Priest | Bard): The player using the heal ability.
            player (str): The name of the character to be healed.
        """
        # Not a priest? Can't heal then.
        if (not isinstance(healer, Priest)) and (not isinstance(healer, Bard)):
            Printer.alert(healer.name + " is not a healer!")
            return
        # Not a valid target?  Return.
        target = self.__in_party(player)
        if not target:
            Printer.alert(player + " is not in the party!")
            return
        # All checks out.  Call healing method.
        amt = healer.heal(target)
        if amt:
            Printer.alert(healer.name + " heals " + target.name + " for " + str(amt) + "hp!")

    '''
    End the game, if and only if the party is currently in the starting dungeon.
    '''
    def __exit(self, *args) -> None:
        """End the game, if and only if the party is currently in the starting dungeon.
        """
        # Not at the exit?  Can't leave.
        if self.__current_location != self.__dungeons[0]:
            Printer.alert("You cannot exit; you aren't at the dungeon exit!")
            return
        # Party dead.  Sadness.  Oh well, YOLO.
        if len(self.__party) == 0:
            Printer.alert("Your party has died in the dungeons.  Alas, there is no one left to mourn you.")
        # Good, maybe we got some gold.
        else:
            Printer.alert("You return with " + str(len(self.__party)) + " members and " + str(self.__gold) + " gold!")
            Printer.alert("Well done, brave warriors!")
            exit(0)

    '''
    Flee back through all the prior dungeons to the exit.
    '''
    def __leave_dungeons(self, *args) -> None:
        """Flee back through all the prior dungeons to the exit.
        """
        while isinstance(self.__current_location.prior, Dungeon) is True:
            self.__retreat()
        else:
            Printer.alert("You are at the entrance.  You must exit to leave.")

    '''
    Print all monsters in the current location and their information
    '''
    def __show_monsters(self, *args):
        """Print all monsters in the current location and their information.
        """
        for monster in self.__current_location.monsters:
            Printer.info(monster)

    '''
    Given a player and the name of an item, remove the item from usage. If it
    is current weapon, or a piece of armor currently being worn, add it to the
    inventory.
    '''
    def __remove(self, player: Character, item_name: str, *args) -> None:
        """Given a player and the name of an item, remove the item from usage.
         If it is current weapon, or a piece of armor currently being worn,
          add it to the inventory.
        Args:
            player (Character): The character that acting.
            item_name (str): The description of the item to remove.
        Except:
            CharacterOverweightException: When performing this action makes
             the player carry too much.
        """
        try:
            _item = self.__find_item(player, item_name)
            if _item:
                player.inventory().append(_item)
                hands = player.in_inventory("Regular Barehanded")
                if hands:
                    player.inventory().remove(hands)
            if player.inventory_weight > player.max_weight:
                raise CharacterOverweightException(player.name + " is carrying too much.", player)
        except CharacterOverweightException as ex:
            Printer.alert("!!!!!! - " + ex.character.name + " is carrying too much weight! - !!!!!!")

    '''
    Print the inventory for a given player.
    '''
    def __player_inventory(self, player: Character, *args) -> None:
        """Print the inventory for a given player.
        Args:
            player (Character): The player whose inventory you want to look at.
        """
        for item in player.inventory():
            Printer.info(item.description)

    '''
    Equipping a weapon adds the weapon's benefits to your stats.
    '''
    def __equip(self, player: Character, item_name: str, *args) -> None:
        """Equipping a weapon adds the weapon's benefits to your stats.
        Args:
            player (Character): The player whose weapon you want to change.
            item_name (str): The description of the item to wield.
        Except:
            CharacterOverweightException: When performing this action makes
             the player carry too much.
        """
        # Weapon not in inventory?  Can't equip it.
        item = player.in_inventory(item_name)
        if item:
            try:
                if isinstance(item, Weapon):
                    player.add_inventory(player.weapon)
                    player.weapon = item
                    player.inventory().remove(item)
                    Printer.info("EQUIPPED " + item.description)
                    hands = player.in_inventory("Regular Barehanded")
                    if hands:
                        player.inventory().remove(hands)
                    if player.inventory_weight > player.max_weight:
                        raise CharacterOverweightException(player.name + " is carrying too much.", player)
                # Not a weapon?  Can't equip it.
                else:
                    Printer.alert("That isn't a weapon; you can't wield it.")
            except CharacterOverweightException as ex:
                Printer.alert("!!!!!! - " + ex.character.name + " is carrying too much weight! - !!!!!!")
        # Don't have that item?  Can't equip it.
        else:
            Printer.alert(player.name + " doesn't have that item in their inventory.")

    '''
    Wearing armor enhances defensive abilities.
    '''
    def __wear(self, player: Character, item_name: str, *args) -> None:
        """Wearing armor enhances defensive abilities.
        Args:
            player (Character): The player whose armor you want to change.
            item_name (str): The description of the item to wear.
        Except:
            CharacterOverweightException: When performing this action makes
             the player carry too much.
        """
        try:
            item = player.in_inventory(item_name)
            if item:
                # Item isn't armor?  Can't wear it.
                if not isinstance(item, Armor):
                    Printer.alert("That is not armor; you can't wear it.")
                    return
                # Already wearing Item of that type?  Switch it out.
                wearing = player.wearing(item.description)
                if wearing:
                    player.add_inventory(wearing)
                    player.armor.remove(wearing)
                    player.armor.append(item)
                else:
                    for armor in player.armor:
                        if armor.type == item.type:
                            player.armor.remove(armor)
                            player.inventory().append(armor)
                    player.armor.append(item)
                    player.inventory().remove(item)
                Printer.info("NOW WEARING " + item.description)
                if player.inventory_weight > player.max_weight:
                    raise CharacterOverweightException(player.name + " is carrying too much.", player)
            else:
                Printer.info("The item " + item_name + " was not found in " + str(player.name) + "'s inventory.")
        except CharacterOverweightException as ex:
            Printer.alert("!!!!!! - " + ex.character.name + " is carrying too much weight! - !!!!!!")

    '''
    Checks if Player is wielding or wearing the Item.
    '''
    def __find_item(self, player: Character, item_name: str, *args) -> Item:
        """Checks if Player is wielding or wearing the Item.
        Args:
            player (Character): The player you want to check.
            item_name (str): The description of the item to check.
        Returns:
            item (Item): The Item being worn or wielded.
        """
        item = item_name
        if player.weapon.description == item_name:
            item = player.weapon
            player.weapon = Weapon(["weapon", "Barehanded", 0, 0, 0])
            player.weapon.condition = ["Regular", 1.0]
        else:
            for armor in player.armor:
                if armor.description == item_name:
                    item = armor
                    player.armor.remove(armor)
        return item

    '''
    Remove the Item from the player's inventory (if exists) and add it to
    the room inventory.
    '''
    def __drop(self, player: Character, item_name: str, *args) -> None:
        """Remove the Item from the player's inventory (if exists) and add
         it to the room inventory.
        Args:
            player (Character): The player dropping the item.
            item_name (str): The description of the item to drop.
        """
        item = player.in_inventory(item_name)
        if item:
            self.__current_location.items.append(item)
            player.inventory().remove(item)
        else:
            Printer.alert(player.name + " does not have that item.")

    '''
    Display player stats.
    '''
    def __stats(self, player: Character, *args) -> None:
        """Display player stats.
        Args:
            player (Character): The player whose stats you want to see.
        """
        Printer.info(player)

    '''
    Move to the next room. If it doesn't exist, make it.
    '''
    def __advance(self, *args) -> None:
        """Move to the next room. If it doesn't exist, make it.
        """
        if isinstance(self.__current_location.next, Dungeon):
            self.__current_location = self.__current_location.next
        else:
            newDungeon = Dungeon("Dungeon Room", "A dark and eerie place that radiates evil.")
            newDungeon.generate()
            self.__current_location.next = newDungeon
            newDungeon.prior = self.__current_location
            self.__current_location = newDungeon
        for monster in self.__current_location.monsters:
            Printer.info(monster)

    '''
    Go back a room.  If at the entrance, you must exit instead.
    '''
    def __retreat(self, *args) -> None:
        """Go back a room.  If at the entrance, you must exit instead.
        """
        if isinstance(self.__current_location.prior, Dungeon) is True:
            self.__current_location = self.__current_location.prior
            print("The party retreats to:\n" + self.__current_location.__str__())
            for monster in self.__current_location.monsters:
                Printer.info(monster)
            self.__monster_attack()
        else:
            Printer.alert("You are at the entrance.  You must exit to leave.")

    '''
    Print the amount of gold in the party.
    '''
    def __see_gold(self, *args) -> None:
        """Print the amount of gold in the party.
        """
        Printer.info("Your party has " + str(self.__gold) + " gold!")

    '''
    See if the player is in the party.  Return them if they are.
    '''
    def __in_party(self, player: str, *args) -> Character | None:
        """See if the player is in the party.  Return them if they are.
        Args:
            player(str): The player to check for.
        Returns:
            warrior (Character | None): Returns the character if they're
             present in the party. None if they're not.
        """
        warrior = None
        for character in self.__party:
            if character.name == player:
                warrior = character
                break
        return warrior

    '''
    If the item is in the room, add it to the inventory.
    '''
    def __take(self, player: Character, target: str, *args) -> None:
        """If the item is in the room, add it to the inventory.
        Args:
            player (Character): The player taking the item.
            target (str): The description of the item to take.
        Exception:
            CharacterOverweightException: When performing this action makes
             the player carry too much.
        """
        try:
            item = None
            for object in self.__current_location.items:
                if object.description == target:
                    item = object
                    owned_item = player.in_inventory(item.description)
                    if owned_item:
                        if item.description == owned_item.description:
                            Printer.alert("You already have a " + item.description + " in your inventory.")
                            return
                    player.add_inventory(object)
                    self.__current_location.items.remove(object)
                    if player.inventory_weight > player.max_weight:
                        raise CharacterOverweightException(player.name + " is carrying too much.", player)
                    break
            if not item:
                Printer.info("You must be seeing things.  There is no " + target + " here!")
        except CharacterOverweightException as ex:
            Printer.alert("!!!!!! - " + ex.character.name + " is carrying too much weight! - !!!!!!")

    '''
    Attempt to attack the target if it is in the room.
    '''
    def __attack(self, player: Character, target: str, *args) -> None:
        """Attempt to attack the target if it is in the room.
        Args:
            player (Character): The player performing the attack.
            target (str): The description of the monster to attack.
        Exception:
            MonsterDeathException: When performing this action results in a monster dying.
        """
        if isinstance(player, Priest):
            Printer.info("----- " + player.name + " refuses to break their vow! -----")
            return
        monster = None
        for mon in self.__current_location.monsters:
            if mon.name == f'{target}\n' or mon.name == target:
                monster = mon
        if not monster:
            Printer.info("There is no monster called " + target + " in this room!")
            return
        try:
            if player.inventory_weight > player.max_weight:
                raise CharacterOverweightException(f"{player.name} can't attack! ", player)
            damage = monster.take_damage(player)
            Printer.alert("----- " + player.name + " attacks " + monster.name +
                          " for " + str(damage) + " damage! -----")
            if monster.health <= 0:
                raise MonsterDeathException(f"{player.name} dealt a killing blow! ", monster)
        except MonsterDeathException as ex:
            Printer.alert("!!!!!! - YES! " + ex.monster.name + " HAS FALLEN! - !!!!!!")
            Printer.info("From its remains you recover " + str(ex.monster.gold) + " gold!")
            self.__gold = self.__gold + ex.monster.gold
            for item in ex.monster.inventory():
                self.__current_location.items.append(item)
            self.__current_location.monsters.remove(ex.monster)
        except CharacterOverweightException as ex:
            Printer.alert("!!!!!! - " + ex.character.name + " can't attack - !!!!!!")
            Printer.info(ex.character.name + "'s inventory is too heavy!")

    '''
    Now the monsters get to attack.
    '''
    def __monster_attack(self) -> None:
        """The monsters in the room attempt to attack your party.
        Exception:
            CharacterDeathException: When performing this action results in a player dying.
        """
        try:
            for monster in self.__current_location.monsters:  # Property object is not iterable TypeError
                character = random.choice(self.__party)
                damage = character.take_damage(monster)
                Printer.alert("----- " + monster.name + " attacks " + character.name
                              + " for " + str(damage) + " damage! -----")
                if character.health <= 0:
                    raise CharacterDeathException(f"{character.name} has died! ", character)
        except CharacterDeathException as ex:
            Printer.alert("!!!!!! - NO! " + ex.character.name + " HAS FALLEN! - !!!!!!")

            ex.character.inventory().append(ex.character.weapon)
            ex.character.weapon = Weapon(["weapon", "Barehanded", 1, 0, 0])
            ex.character.weapon.condition = ["Regular", 1.0]

            hands = ex.character.in_inventory("Regular Barehanded")
            if hands:
                ex.character.inventory().remove(hands)
            for item in ex.character.inventory():
                self.__current_location.items.append(item)
                ex.character.inventory().remove(item)

            for armor in ex.character.armor:
                self.__current_location.items.append(armor)
                ex.character.armor.remove(armor)

            self.__party.remove(ex.character)

    '''
    List all of the commands in the dictionary.
    '''
    def __show_help(self, *args) -> None:
        """Prints off all the commands in the dictionary.
        """
        Printer.info("\nYour options are:\n")
        Printer.info("==========================\n")
        for key in self.__commands.keys():
            Printer.info("\t" + key)

    '''
    Start it up.
    '''
    def __print_welcome(self) -> None:
        """The initial start-up message.
        """
        Printer.dialogue("WELCOME, TRAVELERS!")
        Printer.text("You hear the innkeeper say as your weary party enters the inn.")
        Printer.text("Many days you have been on the road making your way to this town,")
        Printer.text("as you have heard the stories of the precious gold in the nearby")
        Printer.text("dungeons.  After a night or two your party should be well-rested,")
        Printer.text("and ready to claim what other heroes died trying to earn.")
        print()
        Printer.text("What the other travelers don't know, is that your party is different.")
        Printer.text("For you have spent years discerning just the right makeup for a band")
        Printer.text("of warriors, such that you can not only enter the dungeons, but emerge")
        Printer.text("again with your sacks full of gold.")
        Printer.text("First, you have ")
        self.__party.append(self.__choose_player())
        Printer.dialogue("Ah yes, " + self.__party[0].quick_info() + "! They are a formidable foe indeed.")
        Printer.dialogue("But that's, not all - for I also see ")
        self.__party.append(self.__choose_player())
        Printer.dialogue(self.__party[1].quick_info() + ". Few have crossed them"
                                                        " and lived to tell the tale.  And then there is")
        self.__party.append(self.__choose_player())
        Printer.dialogue(self.__party[2].quick_info() + ".  A more noble, and"
                                                        " more loyal friend you could find nowhere.")
        Printer.dialogue("And finally, I notice in the corner")
        self.__party.append(self.__choose_player())
        Printer.dialogue(self.__party[3].quick_info() +
                         ".  Incredible! The legends I have heard of that one shall never")
        Printer.dialogue("be forgotten.")
        print()
        Printer.dialogue("It is late.  Your party should try to sleep...")
        for i in range(0, 8):
            time.sleep(0.25)
            print(".", end='')
        print()
        Printer.info("You awake well rested.")
        self.__party_stats()

    '''
    Print party statistics.
    '''
    def __party_stats(self, *args) -> None:
        """Print party statistics.
        """
        Printer.info("The current statistics of our players are as follows: ")
        for player in self.__party:
            Printer.info(player)

    '''
    Create the four party members.
    '''
    def __choose_player(self) -> Character:
        """Create the four party members.
        Returns:
            player (Character): The Character instance that was created.
        """
        Printer.alert("(What is the name of this player?)")
        name = input()
        while True:
            Printer.info("Choose the class for this player: ")
            Printer.info("\t1. Bard - has healing abilities.")
            Printer.info("\t2. Tank - has extra defense.")
            Printer.info("\t3. DPS - specializes in attacking.")
            Printer.info("\t4. Priest - Blesses the party with increased luck.")
            Printer.info("")
            Printer.alert("Enter your choice (1-4)? ")
            try:
                cls = int(input())
                if cls not in (1, 2, 3, 4):
                    Printer.alert("That is not valid input.")
                    continue
                break
            except ValueError:
                Printer.alert("That is not valid input.")

        player: Optional[Character] = None
        if cls == 1:
            player = Bard(name)
        elif cls == 2:
            player = Tank(name)
        elif cls == 3:
            player = DPT(name)
        else:
            player = Priest(name)
        return player

    '''
    Play the game.
    '''
    def play(self) -> None:
        """Play the game.
        """
        while True:
            if len(self.__party) == 0:
                self.__leave_dungeons()
                self.__exit()
                exit()
            print("Your party is in:\n")

            # Printer.alert("Your party is in:\n")
            print(self.__current_location)
            # Printer.info(self.__current_location)
            cmd = input("What would you like to do? (help or ? for commands): ")
            toks = cmd.split(' ')
            toks = [x.rstrip("\n") for x in toks]
            action = toks[0]
            player = None
            if len(toks) > 1:
                action = toks[1]
                player = self.__in_party(toks[0])
                if not player:
                    Printer.alert("Have you hit your head? " + toks[0] + " is not in this party.")
                    continue
            if action in self.__commands:
                self.__commands[action](player, ' '.join(toks[2:]))
            else:
                Printer.alert("\t>>>>> I don't know what that command means. <<<<<")
            self.__monster_attack()


def main():
    """If the game.py file is run, play the game."""
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
