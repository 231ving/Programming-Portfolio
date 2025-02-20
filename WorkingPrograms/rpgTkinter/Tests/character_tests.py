"""Module containing the unittests for Character.
"""
import unittest
import random
from Classes.character import Character, Player, Enemy
from Classes.item import Item


class CharacterTests(unittest.TestCase):
    """Testcase for the Character class.
    """
    def test_1character_init(self):
        """Check that the Character initializes properly.
        """
        x = Character("Bob", None)
        self.assertEqual(x.name, "Bob")
        self.assertEqual(x.stats["Strength"], 5)
        self.assertEqual(x.stats["Dexterity"], 5)
        self.assertEqual(x.stats["Vitality"], 5)
        self.assertEqual(x.stats["Intelligence"], 5)
        self.assertEqual(x.stats["Level"], 1)
        self.assertEqual(x.stats["XP"], 0)
        self.assertEqual(x.stats["Stat Points"], 5)
        self.assertEqual(x.stats["Credits"], 0)
        self.assertFalse(x.inventory)
        self.assertEqual(x.stats["Max Health"], 20 + (5 * (x.stats["Vitality"] + x.stats["Level"])))
        self.assertEqual(x.stats["Health"], x.stats["Max Health"])
        self.assertEqual(x.attack, 0)
        self.assertEqual(x.defense, 0)
        self.assertTrue(x.living)



    def test_2character_init2(self):
        """Check that the character's stats are initialized."""
        x = Character("Default", {"Strength": 5, "Dexterity": 5, "Vitality": 5,
                      "Intelligence": 5, "Level": 1, "XP": 0, "Stat Points": 5,
                                  "Credits": 0})
        self.assertEqual(x.name, "Default")
        self.assertEqual(x.stats["Strength"], 5)
        self.assertEqual(x.stats["Dexterity"], 5)
        self.assertEqual(x.stats["Vitality"], 5)
        self.assertEqual(x.stats["Intelligence"], 5)
        self.assertEqual(x.stats["Level"], 1)
        self.assertEqual(x.stats["XP"], 0)
        self.assertEqual(x.stats["Stat Points"], 5)
        self.assertEqual(x.stats["Credits"], 0)
        self.assertFalse(x.inventory)
        self.assertEqual(x.stats["Max Health"], 20 + (5 * (x.stats["Vitality"] + x.stats["Level"])))
        self.assertEqual(x.stats["Health"], x.stats["Max Health"])
        self.assertEqual(x.attack, 0)
        self.assertEqual(x.defense, 0)
        self.assertTrue(x.living)

    def test_3set_living(self):
        """Test for the set_living method.
        """
        x = Character("Bob", None)
        x.set_living(False)
        self.assertFalse(x.living)

    def test_4add_item(self):
        """Test for the add_item method.
        """
        x = Character("Bob", None)
        Item.load_items()
        item = Item(random.choice(Item.ITEMS))
        self.assertFalse(x.inventory)
        x.add_item(item)
        self.assertTrue(x.inventory)

    def test_5drop_item(self):
        """Test for the drop_item method.
        """
        x = Character("Bob", None)
        Item.load_items()
        item = Item(random.choice(Item.ITEMS))
        self.assertFalse(x.inventory)
        x.add_item(item)
        x.drop_item(item)
        self.assertFalse(x.inventory)

    def test_6lv_up(self):
        """Test for the lv_up method.
        """
        x = Character("Bob", None)
        x.stats["XP"] += 11
        x.lv_up()
        self.assertEqual(x.stats["Level"], 2)

    def test_7update_max_health(self):
        """Test for the update_max_health method.
        """
        x = Character("Bob", None)
        x.stats["Health"] += 11
        x.update_max_health()
        self.assertEqual(x.stats["Health"], x.stats["Max Health"])

    def test_8update_health(self):
        """Test for the update_health method.
        """
        x = Character("Bob", None)
        x.update_health(100)
        self.assertEqual(x.stats["Health"], x.stats["Max Health"])

    def test_9get_defense(self):
        """Test for the get_defense method.
        """
        x = Character("Bob", None)
        self.assertEqual(x.get_defense(), 0)

    def test_10get_attack(self):
        """Test for the get_attack method.
        """
        x = Character("Bob", None)
        self.assertEqual(x.get_attack(), 0)

    def test_11defend_action(self):
        """Test for the defend_action method.
        """
        x = Character("Bob", None)
        x.defense = 10
        self.assertEqual(x.get_defense(), 10)
        x.defend_action()
        self.assertEqual(x.get_defense(), 15)


class PlayerTests(unittest.TestCase):
    """Testcase for the Player class.
    """
    def test_1player_init1(self):
        """Test that the Player initializes correctly.
        """
        x = Player("Bob", None)
        self.assertEqual(x.name, "Bob")
        self.assertEqual(x.stats["Strength"], 5)
        self.assertEqual(x.stats["Dexterity"], 5)
        self.assertEqual(x.stats["Vitality"], 5)
        self.assertEqual(x.stats["Intelligence"], 5)
        self.assertEqual(x.stats["Level"], 1)
        self.assertEqual(x.stats["XP"], 0)
        self.assertEqual(x.stats["Stat Points"], 5)
        self.assertEqual(x.stats["Credits"], 0)
        self.assertEqual(x.stats["Max Health"], 20 + (5 * (x.stats["Vitality"] + x.stats["Level"])))
        self.assertEqual(x.stats["Health"], x.stats["Max Health"])
        self.assertEqual(x.stats["Medkits"], 5)
        self.assertFalse(x.inventory)
        self.assertIsInstance(x.equipment["Head"], Item)
        self.assertIsInstance(x.equipment["Chest"], Item)
        self.assertIsInstance(x.equipment["Arms"], Item)
        self.assertIsInstance(x.equipment["Legs"], Item)
        self.assertIsInstance(x.equipment["Feet"], Item)
        self.assertIsInstance(x.equipment["Weapon"], Item)
        self.assertTrue(x.attack > 0)
        self.assertTrue(x.defense > 0)
        self.assertTrue(x.living)

    def test_2player_init2(self):
        """Test that the Player's instance attributes are correct.
        """
        x = Player("Default", {"Strength": 5, "Dexterity": 5, "Vitality": 5,
                   "Intelligence": 5, "Level": 1, "XP": 0, "Stat Points": 5,
                               "Credits": 0})
        self.assertEqual(x.name, "Default")
        self.assertEqual(x.stats["Strength"], 5)
        self.assertEqual(x.stats["Dexterity"], 5)
        self.assertEqual(x.stats["Vitality"], 5)
        self.assertEqual(x.stats["Intelligence"], 5)
        self.assertEqual(x.stats["Level"], 1)
        self.assertEqual(x.stats["XP"], 0)
        self.assertEqual(x.stats["Stat Points"], 5)
        self.assertEqual(x.stats["Credits"], 0)
        self.assertEqual(x.stats["Max Health"], 20 + (5 * (x.stats["Vitality"] + x.stats["Level"])))
        self.assertEqual(x.stats["Health"], x.stats["Max Health"])
        self.assertEqual(x.stats["Medkits"], 5)
        self.assertFalse(x.inventory)
        self.assertIsInstance(x.equipment["Head"], Item)
        self.assertIsInstance(x.equipment["Chest"], Item)
        self.assertIsInstance(x.equipment["Arms"], Item)
        self.assertIsInstance(x.equipment["Legs"], Item)
        self.assertIsInstance(x.equipment["Feet"], Item)
        self.assertIsInstance(x.equipment["Weapon"], Item)
        self.assertTrue(x.attack > 0)
        self.assertTrue(x.defense > 0)
        self.assertTrue(x.living)

    def test3_equip_item_real(self):
        """Test for the equip_item method with various Item instances.
        """
        player = Player("Bob", None)
        x = Item(random.choice(Item.ITEMS))
        while x.stats["type"] != "Weapon":
            x = Item(random.choice(Item.ITEMS))
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Weapon"], x)

        while x.stats["type"] != "Head":
            x = Item(random.choice(Item.ITEMS))
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Head"], x)

        while x.stats["type"] != "Arms":
            x = Item(random.choice(Item.ITEMS))
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Arms"], x)

        while x.stats["type"] != "Chest":
            x = Item(random.choice(Item.ITEMS))
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Chest"], x)

        while x.stats["type"] != "Legs":
            x = Item(random.choice(Item.ITEMS))
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Legs"], x)

        while x.stats["type"] != "Feet":
            x = Item(random.choice(Item.ITEMS))
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Feet"], x)

    def test4_equip_item_none_item(self):
        """Test for the equip_item method if the Item's have a name of "None".
        """
        player = Player("Bob", None)
        x = Item(["Weapon", "None", 0, 0, 0, 0.8])
        player.equipment["Weapon"] = x
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Weapon"], x)

        x = Item(["Head", "None", 0, 0, 0, 0.8])
        player.equipment["Head"] = x
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Head"], x)

        x = Item(["Chest", "None", 0, 0, 0, 0.8])
        player.equipment["Chest"] = x
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Chest"], x)

        x = Item(["Arms", "None", 0, 0, 0, 0.8])
        player.equipment["Arms"] = x
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Arms"], x)

        x = Item(["Legs", "None", 0, 0, 0, 0.8])
        player.equipment["Legs"] = x
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Legs"], x)

        x = Item(["Feet", "None", 0, 0, 0, 0.8])
        player.equipment["Feet"] = x
        player.add_item(x)
        player.equip_item(x)
        self.assertEqual(player.equipment["Feet"], x)

    def test_5unequip_item_real(self):
        """Test for the unequip_item method with various Item instances.
        """
        player = Player("Bob", None)
        x = player.equipment["Weapon"]
        player.unequip_item(x)
        unequipped = None
        for item in player.inventory:
            if item == x:
                unequipped = item
        self.assertEqual(x, unequipped)

        x = player.equipment["Head"]
        player.unequip_item(x)
        unequipped = None
        for item in player.inventory:
            if item == x:
                unequipped = item
        self.assertEqual(x, unequipped)

        x = player.equipment["Arms"]
        player.unequip_item(x)
        unequipped = None
        for item in player.inventory:
            if item == x:
                unequipped = item
        self.assertEqual(x, unequipped)

        x = player.equipment["Chest"]
        player.unequip_item(x)
        unequipped = None
        for item in player.inventory:
            if item == x:
                unequipped = item
        self.assertEqual(x, unequipped)

        x = player.equipment["Legs"]
        player.unequip_item(x)
        unequipped = None
        for item in player.inventory:
            if item == x:
                unequipped = item
        self.assertEqual(x, unequipped)

        x = player.equipment["Feet"]
        player.unequip_item(x)
        unequipped = None
        for item in player.inventory:
            if item == x:
                unequipped = item
        self.assertEqual(x, unequipped)

    def test_6unequip_item_none(self):
        """Test for the unequip_item method if the Items have the name "None".
        """
        player = Player("Bob", None)
        x = Item(["Weapon", "None", 0, 0, 0, 0.8])
        player.equipment["Weapon"] = x
        player.equip_item(x)
        player.unequip_item(x)
        self.assertEqual(player.inventory, [])

        x = Item(["Head", "None", 0, 0, 0, 0.8])
        player.equipment["Head"] = x
        player.equip_item(x)
        player.unequip_item(x)
        self.assertFalse(player.inventory)

        x = Item(["Chest", "None", 0, 0, 0, 0.8])
        player.equipment["Chest"] = x
        player.equip_item(x)
        player.unequip_item(x)
        self.assertFalse(player.inventory)

        x = Item(["Arms", "None", 0, 0, 0, 0.8])
        player.equipment["Arms"] = x
        player.equip_item(x)
        player.unequip_item(x)
        self.assertFalse(player.inventory)

        x = Item(["Legs", "None", 0, 0, 0, 0.8])
        player.equipment["Legs"] = x
        player.equip_item(x)
        player.unequip_item(x)
        self.assertFalse(player.inventory)

        x = Item(["Feet", "None", 0, 0, 0, 0.8])
        player.equipment["Feet"] = x
        player.equip_item(x)
        player.unequip_item(x)
        self.assertFalse(player.inventory)

    def test_7use_medkits(self):
        """Test for the use_medkits method.
        """
        player = Player("Bob", None)
        player.use_medkits()
        self.assertEqual(player.stats["Medkits"], 4)
        player.stats["Health"] = 1
        player.use_medkits()
        self.assertTrue(player.stats["Health"] > 1)
        player.stats["Medkits"] = 0
        player.use_medkits()
        self.assertEqual(player.stats["Medkits"], 0)

    def test_8get_medkits(self):
        """Test for the medkits property.
        """
        player = Player("Bob", None)
        self.assertEqual(player.med_kits, 5)

    def test_9set_medkits(self):
        """Test for the medkits setter.
        """
        player = Player("Bob", None)
        player.med_kits = -1
        self.assertEqual(player.med_kits, 4)

        player.med_kits = -100
        self.assertEqual(player.med_kits, 0)

    def test_10change_name(self):
        """Test for the change_name method.
        """
        player = Player("Bob", None)
        player.change_name("SD")
        self.assertEqual(player.name, "SD")

    def test_11update_defense(self):
        """Test for the update_defense method.
        """
        player = Player("Bob", None)
        defense = player.get_defense()
        player.stats["Vitality"] += 5
        player.update_defense()
        self.assertTrue(player.get_defense() > defense)

    def test_12update_attack(self):
        """Test for the update_attack method.
        """
        player = Player("Bob", None)
        attack = player.get_attack()
        player.stats["Strength"] += 5
        player.update_attack()
        self.assertTrue(player.get_attack() > attack)

    def test_13take_damage(self):
        """Test for the take_damage method.
        """
        player = Player("Bob", None)
        health = player.stats["Health"]
        x = player.take_damage(player)
        while x != 0:
            x = player.take_damage(player)
            player.update_health(x)
        self.assertEqual(x, 0)
        while player.stats["Health"] > 0:
            player.take_damage(player)
            self.assertTrue(player.stats["Health"] < health)

    def test_14take_damage_killed(self):
        """Test that the take_damage method sets the Player's status to be dead.
        """
        player = Player("Bob", None)
        player.stats["Health"] = 1
        while player.living is True:
            player.take_damage(player)
        self.assertFalse(player.living)



class EnemyTests(unittest.TestCase):
    """Testcase for the Enemy class.
    """
    def test_1enemy_init1(self):
        """Test for the Enemy instance initialization.
        """
        x = Enemy("Bob", None, 1)
        self.assertEqual(x.name, "Bob")
        self.assertTrue(x.stats["Strength"] >= 5)
        self.assertTrue(x.stats["Dexterity"] >= 5)
        self.assertTrue(x.stats["Vitality"] >= 5)
        self.assertTrue(x.stats["Intelligence"] >= 5)
        self.assertEqual(x.stats["Level"], 1)
        self.assertEqual(x.stats["XP"], 0)
        self.assertEqual(x.stats["Stat Points"], 0)
        self.assertEqual(x.stats["Credits"], 0)
        self.assertEqual(x.stats["Max Health"], 20 + (5 * (x.stats["Vitality"] + x.stats["Level"])))
        self.assertEqual(x.stats["Health"], x.stats["Max Health"])
        self.assertFalse(x.inventory)
        self.assertTrue(x.attack > 0)
        self.assertTrue(x.defense > 0)
        self.assertTrue(x.living)

    def test_2enemy_init2(self):
        """Test for the instance attributes.
        """
        x = Enemy("Bob", None, 10)
        self.assertEqual(x.stats["Level"], 10)
        self.assertEqual(x.name, "Bob")
        self.assertTrue(x.stats["Strength"] > 5)
        self.assertTrue(x.stats["Dexterity"] > 5)
        self.assertTrue(x.stats["Vitality"] > 5)
        self.assertTrue(x.stats["Intelligence"] > 5)
        self.assertEqual(x.stats["XP"], 0)
        self.assertEqual(x.stats["Stat Points"], 0)
        self.assertEqual(x.stats["Credits"], 0)
        self.assertEqual(x.stats["Max Health"], 20 + (5 * (x.stats["Vitality"] + x.stats["Level"])))
        self.assertEqual(x.stats["Health"], x.stats["Max Health"])
        self.assertFalse(x.inventory)
        self.assertTrue(x.attack > 0)
        self.assertTrue(x.defense > 0)
        self.assertTrue(x.living)

    def test_3take_damage(self):
        """Test for the take_damage method.
        """
        enemy = Enemy("Bob", None, 10)
        player = Player("Ded", None)
        health = enemy.stats["Health"]
        enemy.take_damage(player)
        while enemy.stats["Health"] >= health:
            enemy.take_damage(player)
        self.assertTrue(enemy.stats["Health"] < health)
        player.unequip_item(player.equipment["Weapon"])
        player.damage = 0
        enemy.take_damage(player)
        self.assertTrue(enemy.stats["Health"] < health)

    def test_4update_defense(self):
        """Test for the update_defense method.
        """
        enemy = Enemy("Bob", None, 10)
        defense = enemy.get_defense()
        enemy.stats["Vitality"] += 10
        enemy.update_defense()
        self.assertTrue(enemy.get_defense() > defense)

    def test_5update_attack(self):
        """Test for the update_attack method.
        """
        enemy = Enemy("Bob", None, 10)
        attack = enemy.get_attack()
        enemy.stats["Strength"] += 10
        enemy.update_attack()
        self.assertTrue(enemy.get_attack() > attack)

    def test_6update_stats(self):
        """Test for the update_stats method.
        """
        enemy = Enemy("Bob", None, 1)
        stat_sum = (enemy.stats["Strength"] + enemy.stats["Dexterity"] +
                    enemy.stats["Vitality"] + enemy.stats["Intelligence"])
        enemy.stats["Stat Points"] += 10
        enemy.update_stats()
        final_stat_sum = (enemy.stats["Strength"] + enemy.stats["Dexterity"] +
                          enemy.stats["Vitality"] +
                          enemy.stats["Intelligence"])
        self.assertTrue(final_stat_sum > stat_sum)

    def test_7randomize_action(self):
        """Test the randomize_action method"""
        enemy = Enemy("Bob", None, 1)
        enemy_action = enemy.action
        while enemy_action == enemy.action:
            enemy.randomize_action()
        self.assertTrue(enemy.action != enemy_action)
        self.assertTrue(enemy.action in enemy.actions)

    def test_8set_action(self):
        """Test the set_action method"""
        enemy = Enemy("Bob", None, 1)
        enemy_actions = len(enemy.actions)
        enemy.set_actions("dodge")
        self.assertTrue(len(enemy.actions) > enemy_actions)
        self.assertTrue("dodge" in enemy.actions)
