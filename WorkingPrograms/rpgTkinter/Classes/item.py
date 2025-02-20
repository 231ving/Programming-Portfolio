"""Module for the Item class.
"""
import random
import csv


class Item:
    """Class containing various details about an item.
     ITEMS is the list containing all possible item details.
    """

    ITEMS = []

    @staticmethod
    def load_items() -> None:
        """Static method to load the different types of items
         from a specified file.
        """
        if not Item.ITEMS:
            with open('Names/items_txt/item_types', 'r',
                      encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    Item.ITEMS.append(row)

    def __init__(self, stats: list):
        """Creates the Item instance.
        Args:
            stats (list): The 5-element list of item details.
             Must follow the format below.
        """
        if not Item.ITEMS:
            Item.load_items()

        self.stats = {"type": stats[0], "name": stats[1],
                      "damage": int(stats[2]), "defense": int(stats[3]),
                      "value": int(stats[4]), "damagePercent": float(stats[5]),
                      "critPercent": 0.1, "armorBreakPercent": 0.1}
        self.name = "None"
        self.damage = 0
        self.damage_percent = 0
        self.crit_percent = 0
        self.armor_break_percent = 0
        self.assign_stats()

    def assign_stats(self):
        """Method to assign additional stats to an item.
        """
        self.name = self.stats["name"]
        self.damage = self.stats["damage"]

        # What % Higher or % Lower from self.damage can possible damages be
        self.damage_percent = self.stats["damagePercent"]

        # In the format 0.%%
        self.crit_percent = self.stats["critPercent"]

        # Chance of damage bypassing enemies defense
        self.armor_break_percent = self.stats["armorBreakPercent"]

        # More stats can be added but idk

    # Enemy would be an instance of the enemy class
    def get_damage_dealt(self, enemy):
        """Method to calculate the item's damage to a specified enemy.
        Args:
            enemy (Character): The enemy the item would be attacking.
        Returns:
            float: The calculated damage dealt by this Item.
        """
        damage_range_value = random.uniform(1 - self.damage_percent,
                                            1 + self.damage_percent)
        base_damage_dealt = self.damage * damage_range_value

        applied_damage = base_damage_dealt
        if random.random() < self.crit_percent:
            applied_damage *= 2

        # If crit is
        enemy_defense_reducer = 1
        if random.random() < self.armor_break_percent:
            enemy_defense_reducer = 0.5

        enemy_defense = enemy.get_defense()

        return applied_damage - enemy_defense * enemy_defense_reducer
