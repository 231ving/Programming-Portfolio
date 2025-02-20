"""
Run Tests from Here. Do not run the test files in the Test Folder.
"""

import unittest
from Tests.map_tests import MapTests
from Tests.edge_tests import EdgeTests
from Tests.item_tests import ItemTests
from Tests.character_tests import CharacterTests, PlayerTests, EnemyTests
from Tests.room_tests import RoomTests
from Tests.shop_room_tests import ShopRoomTests
from Tests.chest_room_tests import ChestRoomTests
from Tests.combat_room_tests import CombatRoomTests
from Tests.start_room_tests import StartRoomTests
from Tests.boss_room_tests import BossRoomTests


test_suite = unittest.TestSuite()

# Add to suite for each method in test class
# Map Tests
test_suite.addTests([MapTests('test1_map_init'),
                     MapTests('test2_generate_map'),
                     MapTests('test3_get_current_room'),
                     MapTests('test4_set_current_room'),
                     MapTests('test5_generate_random_rooms'),
                     MapTests('test6_connect_every_room_together'),
                     MapTests('test7_prims_algorithm'),
                     MapTests('test8_assign_random_images'),
                     MapTests('test9_assign_random_images_round2'),
                     MapTests('test10_print_map')])
# Edge Tests
test_suite.addTests([EdgeTests('test1'), EdgeTests('test2'),
                     EdgeTests('test3')])
# Item Tests
test_suite.addTests([ItemTests('test_1load_items1'),
                     ItemTests('test_2load_items2'),
                     ItemTests('test_3load_items3'),
                     ItemTests('test_4load_items4'),
                     ItemTests('test_5item_init'),
                     ItemTests('test_6item_assign_stats'),
                     ItemTests('test_7item_get_damage'),
                     ItemTests('test_8item_notitem')])
# Character Tests
test_suite.addTests([CharacterTests('test_1character_init'),
                     CharacterTests('test_2character_init2'),
                     CharacterTests('test_3set_living'),
                     CharacterTests('test_4add_item'),
                     CharacterTests('test_5drop_item'),
                     CharacterTests('test_6lv_up'),
                     CharacterTests('test_7update_max_health'),
                     CharacterTests('test_8update_health'),
                     CharacterTests('test_9get_defense'),
                     CharacterTests('test_10get_attack'),
                     CharacterTests('test_11defend_action')])
# Player Tests
test_suite.addTests([PlayerTests('test_1player_init1'),
                     PlayerTests('test_2player_init2'),
                     PlayerTests('test3_equip_item_real'),
                     PlayerTests('test4_equip_item_none_item'),
                     PlayerTests('test_5unequip_item_real'),
                     PlayerTests('test_6unequip_item_none'),
                     PlayerTests('test_7use_medkits'),
                     PlayerTests('test_8get_medkits'),
                     PlayerTests('test_9set_medkits'),
                     PlayerTests('test_10change_name'),
                     PlayerTests('test_11update_defense'),
                     PlayerTests('test_12update_attack'),
                     PlayerTests('test_13take_damage'),
                     PlayerTests('test_14take_damage_killed')])
# Enemy Tests
test_suite.addTests([EnemyTests('test_1enemy_init1'),
                     EnemyTests('test_2enemy_init2'),
                     EnemyTests('test_3take_damage'),
                     EnemyTests('test_4update_defense'),
                     EnemyTests('test_5update_attack'),
                     EnemyTests('test_6update_stats'),
                     EnemyTests('test_7randomize_action'),
                     EnemyTests('test_8set_action')])
# Room Tests
test_suite.addTests([RoomTests('test_1room_init'),
                     RoomTests('test_2set_coordinates'),
                     RoomTests('test_3get_coordinates'),
                     RoomTests('test_4clear_room'),
                     RoomTests('test_5get_cleared'),
                     RoomTests('test_6create_adjacency'),
                     RoomTests('test_7create_adjacency_alreadyadjacent'),
                     RoomTests('test_8add_adjacent_room'),
                     RoomTests('test_9get_adjacent_rooms'),
                     RoomTests('test_10generate_name'),
                     RoomTests('test_11generate_name_round2'),
                     RoomTests('test_12__repr__'),
                     RoomTests('test_13__eq__')])
# ChestRoom Tests
test_suite.addTest(ChestRoomTests('test_1chestroom_init'))
# CombatRoom Tests
test_suite.addTests([CombatRoomTests('test_1combatroom_init'),
                     CombatRoomTests('test_2generate_enemies'),
                     CombatRoomTests('test_3generate_enemies_player_exists'),
                     CombatRoomTests('test_4lv_enemies')])
# ShopRoom Tests
test_suite.addTest(ShopRoomTests('test_1shoproom_init'))
# StartRoom Tests
test_suite.addTest(StartRoomTests('test_1startroom_init'))
# BossRoom Tests
test_suite.addTests([BossRoomTests('test_1bossroom_init'), BossRoomTests('test_2lv_boss')])
# ...

runner = unittest.TextTestRunner(verbosity=2)
runner.run(test_suite)
