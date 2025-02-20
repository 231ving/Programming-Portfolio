"""
The Character Module. Contains the generic Character class, the Player class,
 and the Enemy class.
"""

import random

from Classes.item import Item

if not Item.ITEMS:
    Item.load_items()


class Character:
    """The generic Character class.
     Used as a parent for the more specialized Player and Enemy classes.
    """
    def __init__(self, name: str, stats=None):
        """Creates the character.
        Args:
            name (str):
            stats (None | dict): None gets the default stats below.
             A dictionary lets you make a character of a higher level.
        """
        if stats is None:
            stats = {"Strength": 5, "Dexterity": 5, "Vitality": 5,
                     "Intelligence": 5, "Level": 1, "XP": 0, "Stat Points": 5,
                     "Credits": 0}
        self.name = name
        self.inventory = []
        self.stats = stats
        self.stats["Max Health"] = 20 + (5 * (self.stats["Vitality"]
                                              + self.stats["Level"]))
        self.stats["Health"] = self.stats["Max Health"]
        self.attack = 0  # Pull item attack + character strength?
        self.defense = 0  # Pull item defense + character vitality?
        self.living = True
        self.is_in_combat = False

    def set_living(self, _bool):
        """Setter for the living attribute.
        Args:
            _bool (bool): Boolean value for the character's living status.
        """
        self.living = _bool

    def add_item(self, item: Item):
        """Adds an Item to the character's inventory.
        Args:
            item (Item): Requires an Item object.
        """
        self.inventory.append(item)

    def drop_item(self, item: Item):
        """Removes an Item from the character's inventory.
        Args:
            item (Item): Requires an Item object.
        """
        self.inventory.remove(item)

    # Upgrade stats by stat and amount
    def upgrade_stats(self, stat, amount):
        """Method to upgrade a character's stats.
        Args:
            stat (str): The stat to increase.
            amount (int): How much to increase the stat by.
        """
        if self.stats["Stat Points"] > 0:
            self.stats[stat] += amount
            self.stats["Stat Points"] -= amount
            if stat == "Vitality":
                self.update_max_health()
                self.update_health(5 * amount)

    def lv_up(self):
        """Tries to level up the character if they have enough XP.
        Adds unassigned stat points if they do.
        """
        if self.stats["XP"] >= (self.stats["Level"] * 10):
            self.stats["XP"] -= self.stats["Level"] * 10
            self.stats["Level"] += 1
            self.stats["Stat Points"] += 5

    def update_max_health(self):
        """Recalculates the character's Max Health."""
        self.stats["Max Health"] = 20 + (5 * (self.stats["Vitality"]
                                              + self.stats["Level"]))
        if self.stats["Health"] > self.stats["Max Health"]:
            self.stats["Health"] = self.stats["Max Health"]

    def update_health(self, amount: int):
        """Changes the character's current Health by amount.
        Args:
            amount (int): How much to change the character's Health by.
        """
        self.stats["Health"] += amount
        if self.stats["Health"] > self.stats["Max Health"]:
            self.stats["Health"] = self.stats["Max Health"]

    def get_defense(self):
        """Getter for the character's defense attribute.
        Returns:
            defense (int): The character's defense, including
             equipment bonuses.
        """
        return self.defense

    def get_attack(self):
        """Getter for the character's attack attribute.
                Returns:
                    attack (int): The character's attack, including
                     weapon bonuses.
                """
        return self.attack

    def defend_action(self):
        """Method to increase character's defense.
        """
        self.defense = int(self.defense * 1.5)


class Player(Character):
    """Child class of Character. Specialized to be the player character.
    Adds medkits for healing and the ability to use equipment.
    """
    def __init__(self, name: str, stats: dict):
        """Same idea as the parent Character class.
        """
        super().__init__(name, stats)
        self.stats["Medkits"] = 5

        self.equipment = {}
        x = Item(random.choice(Item.ITEMS))
        while x.stats["type"] != "Weapon":
            x = Item(random.choice(Item.ITEMS))
        self.equipment["Weapon"] = x
        while x.stats["type"] != "Head":
            x = Item(random.choice(Item.ITEMS))
        self.equipment["Head"] = x
        while x.stats["type"] != "Arms":
            x = Item(random.choice(Item.ITEMS))
        self.equipment["Arms"] = x
        while x.stats["type"] != "Chest":
            x = Item(random.choice(Item.ITEMS))
        self.equipment["Chest"] = x
        while x.stats["type"] != "Legs":
            x = Item(random.choice(Item.ITEMS))
        self.equipment["Legs"] = x
        while x.stats["type"] != "Feet":
            x = Item(random.choice(Item.ITEMS))
        self.equipment["Feet"] = x
        self.update_attack()
        self.update_defense()

    def equip_item(self, item: Item):
        """Method for the Player to equip an item from their inventory.
        Args:
            item (Item): The item to be equipped from the Player's inventory.
        """
        if item in self.inventory:
            for item_type in ["Weapon", "Head", "Chest",
                              "Arms", "Legs", "Feet"]:
                if item.stats["type"] == item_type:
                    if self.equipment[item_type].stats["name"] == "None":
                        self.equipment[item_type] = item
                    else:
                        tmp = self.equipment[item_type]
                        self.equipment[item_type] = item
                        self.add_item(tmp)
            self.inventory.remove(item)
            self.update_attack()
            self.update_defense()

    def unequip_item(self, item: Item):
        """Method for the Player to unequip an item from their equipment
         and place it into their inventory.
        Args:
            item (Item): The item to be unequipped from the Player's equipment.
        """
        for item_type in ["Weapon", "Head", "Chest", "Arms", "Legs", "Feet"]:
            if item.stats["type"] == item_type:
                if item.stats["name"] != "None":
                    self.add_item((self.equipment[item_type]))
                self.equipment[item_type] = Item([item_type, "None", 0,
                                                  0, 0, 0.8])
        self.update_attack()
        self.update_defense()

    def use_medkits(self):
        """Method to heal by spending a medkit.
        Returns:
            amt (int): The amount the medkit healed the Player for. 0 if no
             medkit was used.
        """
        amt = 0
        if self.med_kits > 0:
            self.med_kits = -1
            amt = self.stats["Intelligence"] + self.stats["Level"] + 20
            tmp = self.stats["Health"] + amt
            if tmp >= self.stats["Max Health"]:
                amt = self.stats["Max Health"] - self.stats["Health"]
                self.stats["Health"] = self.stats["Max Health"]
            else:
                self.stats["Health"] = tmp
            print(self.name + " used a med kit and healed for " + str(amt)
                  + " health.")
        else:
            print("No med kits left.")
        return amt

    @property
    def med_kits(self) -> int:
        """Getter for the Player's medkits.
        Returns:
            stats["Medkits"] (int): The number of medkits the Player has.
        """
        return self.stats["Medkits"]

    @med_kits.setter
    def med_kits(self, change: int):
        """Changes the number of medkits by change.
        Args:
            change (int): How much the medkits are being changed by.
        """
        self.stats["Medkits"] += change
        if self.stats["Medkits"] < 0:
            self.stats["Medkits"] = 0

    def change_name(self, name):
        """Method to change the Player's name.
        Returns:
            name (str): The player's new name.
        """
        self.name = name

    def update_defense(self):
        """Updates the Player's defense attribute.
        """
        self.defense = int((self.stats["Vitality"] + self.stats["Level"]) / 3)
        for equipment in self.equipment.values():
            self.defense += equipment.stats["defense"]

    def update_attack(self):
        """Updates the Player's attack attribute.
        """
        self.attack = int((self.stats["Strength"] + self.stats["Level"]) / 3)
        for equipment in self.equipment.values():
            self.attack += equipment.stats["damage"]

    def take_damage(self, attacker: Character):
        """Method used when a Player takes damage.
        Args:
            attacker (Character): The Character object that is attacking
             the Player.
        """
        damage = attacker.get_attack() - self.get_defense() / 3
        damage = max(int(damage), 1)
        attacker_hit_chance = (random.randint(1, 100) + damage +
                               attacker.stats["Dexterity"]
                               + attacker.stats["Level"])
        defender_dodge_chance = (random.randint(1, 100) + damage +
                                 self.stats["Dexterity"] + self.stats["Level"])
        if attacker_hit_chance > defender_dodge_chance:
            self.stats["Health"] -= int(damage)
        else:
            damage = 0

        # Set state of character
        if self.stats["Health"] <= 0:
            self.set_living(False)
        return damage


class Enemy(Character):
    """Child of the Character class. Specialzed for enemies specifically.
    Allows for enemies' stats to scale based on an input level.
    """
    def __init__(self, name: str, stats: dict, enemy_lv: int):
        """Creates the Enemy object.
        New Args:
            enemy_lv (int): The level the enemy is scaled to.
        """
        super().__init__(name, stats)
        self.stats["Level"] = enemy_lv
        self.stats["Stat Points"] = self.stats["Level"] * 5
        self.action = "nothing"
        self.actions = ["attack", "defend", "nothing"]
        self.update_stats()
        self.stats["Health"] = self.stats["Max Health"]
        self.update_attack()
        self.update_defense()
        self.randomize_action()

    def take_damage(self, attacker: Player):
        """Method for the Enemy to take damage.
        Returns:
            attacker (Player): Player instance that is attacking.
        """
        item = attacker.equipment["Weapon"]
        damage = (item.get_damage_dealt(self) + attacker.get_attack()
                  - self.get_defense() / 2)
        damage = max(int(damage), 1)
        attacker_hit_chance = (random.randint(1, 100) + damage +
                               attacker.stats["Dexterity"]
                               + attacker.stats["Level"])
        defender_dodge_chance = (random.randint(1, 100) + damage +
                                 self.stats["Dexterity"] + self.stats["Level"])
        if attacker_hit_chance > defender_dodge_chance:
            self.stats["Health"] -= int(damage)
        else:
            damage = 0
        self.stats["Health"] -= damage
        return damage

    def update_defense(self):
        """Updates the Enemy's defense attribute.
        """
        self.defense = int((self.stats["Vitality"] / 3) + self.stats["Level"])

    def update_attack(self):
        """Updates the Enemy's defense attribute.
        """
        self.attack = int((self.stats["Strength"] / 3) + self.stats["Level"])

    def update_stats(self):
        """Randomly increases the Enemy's stats until they're out
         of Stat Points.
        """
        while self.stats["Stat Points"] >= 1:
            stat = random.choice(['Strength', 'Dexterity',
                                  'Vitality', 'Intelligence'])
            self.upgrade_stats(stat, 1)

    def randomize_action(self):
        """Randomize the Enemy instance's chosen action.
        """
        self.action = random.choice(self.actions)

    def set_actions(self, action: str):
        """Adds new action to the Enemy instance's choices.
        Args:
            action (str): The action to be added. Action functionality is not
             guaranteed without a corresponding method.
        """
        if isinstance(action, str):
            self.actions.append(action)
