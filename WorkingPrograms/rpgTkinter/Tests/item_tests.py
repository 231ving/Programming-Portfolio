"""Module containing unittests for the Item class.
"""
import random
import unittest
from Classes.item import Item
from Classes.character import Enemy


class ItemTests(unittest.TestCase):
    """Testcase for the Item class.
    """

    def test_1load_items1(self):
        """Test that the list of item details loads properly.
        """
        self.assertFalse(not Item.ITEMS)

    def test_2load_items2(self):
        """Test that the list of item details exists.
        """
        self.assertTrue(Item.ITEMS)

    def test_3load_items3(self):
        """Test that the load_items static method works.
        """
        Item.load_items()
        self.assertTrue(Item.ITEMS)

    def test_4load_items4(self):
        """Test that multiple load_item methods don't duplicate the same entry.
        """
        Item.load_items()
        x = len(Item.ITEMS)
        self.assertEqual(len(Item.ITEMS), x)
        Item.load_items()
        self.assertEqual(len(Item.ITEMS), x)

    def test_5item_init(self):
        """Test that the Item instance initializes properly.
        """
        Item.load_items()
        stats = random.choice(Item.ITEMS)
        x = Item(stats)
        item_type = stats[0]
        name = stats[1]
        damage = int(stats[2])
        defense = int(stats[3])
        value = int(stats[4])
        damagepercent = float(stats[5])
        self.assertEqual(x.stats["type"], item_type)
        self.assertEqual(x.stats["name"], name)
        self.assertEqual(x.stats["damage"], damage)
        self.assertEqual(x.stats["defense"], defense)
        self.assertEqual(x.stats["value"], value)
        self.assertEqual(x.stats["damagePercent"], damagepercent)

    def test_6item_assign_stats(self):
        """Test that the assignStats method works.
        """
        Item.load_items()
        stats = random.choice(Item.ITEMS)
        x = Item(stats)
        x.assign_stats()
        self.assertEqual(x.stats["name"], x.name)
        self.assertEqual(x.stats["damage"], x.damage)
        self.assertEqual(x.stats["armorBreakPercent"], x.armor_break_percent)
        self.assertEqual(x.stats["critPercent"], x.crit_percent)
        self.assertEqual(x.stats["damagePercent"], x.damage_percent)

    def test_7item_get_damage(self):
        """Test that the get_damage_dealt method works.
        """
        Item.load_items()
        stats = random.choice(Item.ITEMS)
        x = Item(stats)
        enemy = Enemy("Tester", None, 1)
        self.assertTrue(x.get_damage_dealt(enemy))

    def test_8item_notitem(self):
        """Test that a new Item instance doesn't duplicate the ITEMS list.
        """
        stats = random.choice(Item.ITEMS)
        Item(stats)
        Item.load_items()
        self.assertTrue(Item.ITEMS, Item.ITEMS)
