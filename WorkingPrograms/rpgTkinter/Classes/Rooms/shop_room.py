"""Module for the ShopRoom class.
"""
import random
from Classes.Rooms.room import Room
from Classes.item import Item


class ShopRoom(Room):
    """Specialized room the player can buy items in.
    """
    def __init__(self):
        """Creates the instance with a random number of items to sell.
        """
        super().__init__()
        self.name = self.generate_name("Shop")
        self.room_type = "Shop"
        self.items = []

        num_items = random.randint(1, 4)
        for _ in range(0, num_items):
            self.items.append(Item(random.choice(Item.ITEMS)))

        self.text = "You have entered a Shop room. Prepare to buy items."
