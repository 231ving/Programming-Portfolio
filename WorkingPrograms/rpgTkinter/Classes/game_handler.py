"""Module for the GameHandler class.
"""
import math
import time
import random
import datetime
from Classes.GUI.chest_gui import ChestGUI
from Classes.GUI.fight_gui import FightGUI
from Classes.GUI.main_gui import MainGUI
from Classes.GUI.shop_gui import ShopGUI
from Classes.character import Player
from Classes.Map.map import Map
from Classes.save_manager import SaveManager


class GameHandler:
    """Manages the various game events.
    """
    counter = 1

    def __init__(self):
        """Creates the instance.
        """
        self.player = Player("Default", {"Strength": 5, "Dexterity": 5,
                                         "Vitality": 5, "Intelligence": 5,
                                         "Level": 1, "XP": 0, "Stat Points": 5,
                                         "Credits": 1000})
        self.map = Map()
        self.initial_time = time.time()
        self.total_enemies_killed = 0
        self.total_rooms_entered = 0
        self.round = GameHandler.counter

        self.gui = None
        self.save_manager = SaveManager()
        MainGUI(self.player, self)

    def start_from_save(self, save):
        """Starts a game from a save instead of creating a new game.
        Args:
            save: The save file to get the data from
        """
        GameHandler.counter = save["Round_Number"]

        self.total_rooms_entered = save["sessions_stats"]["rooms_entered"]
        self.total_enemies_killed = save["sessions_stats"]["enemies_killed"]


        self.player = save["Player"]
        self.map = save["Map"]

        self.gui.create_main_gui()

    def start_new_game(self):
        """Starts a new game.
        """

        old_name = self.player.name
        self.player = Player(old_name, {"Strength": 5, "Dexterity": 5,
                                        "Vitality": 5, "Intelligence": 5,
                                        "Level": 1, "XP": 0, "Stat Points": 5,
                                        "Credits": 0})

        # Reset game stats
        self.initial_time = time.time()
        self.total_enemies_killed = 0
        self.total_rooms_entered = 0
        self.round = GameHandler.counter

        self.map = Map()
        self.gui.create_main_gui()

    def start_next_map(self):
        """Creates a new map for the player if they want to continue.
        """

        GameHandler.counter += 1
        self.round = GameHandler.counter  # Variable to increase each level.
        if GameHandler.counter > 3:
            GameHandler.counter = random.randint(1, 3)

        self.map = Map()
        self.gui.create_main_gui()

    def get_map(self):
        """Getter for the map attribute.
        Returns:
            map (Map): The Map instance.
        """
        return self.map

    # For some reason python isn't happy if I set MainGUI above to a variable
    # so I have to do this
    def set_gui(self, gui):
        """Setter for the GUI attribute.
        Args:
            gui (MainGUI): The MainGUI instance.
        """
        self.gui = gui

    def enter_room(self, room):
        """Method to enter a different room.
        Args:
            room (Room): The room in the map to enter.
        Returns:
            None: If a room event is still ongoing.
             i.e. Another window is still active.
        """
        self.map.set_current_room(room)
        self.gui.display_buttons()

        if room.cleared:
            self.gui.enter_repeated_room(room)
            return

        self.total_rooms_entered += 1

        match room.room_type:
            case "Combat":
                room.player = self.player
                room.lv_enemies()
                self.gui.enter_combat_room(room)
                FightGUI(room, self.player, self)
            case "Chest":
                self.gui.enter_chest_room(room)
                ChestGUI(room, self.player, self)
            case "Shop":
                self.gui.enter_shop_room(room)
                ShopGUI(room, self.player, self)
            case "Boss":
                if self.round > 1:
                    room.lv_boss(5 * (self.round - 1))
                self.gui.enter_boss_room(room)
                FightGUI(room, self.player, self)
            case "Start":
                room.clear_room(True)

    def exit_room(self, room):
        """Method to exit a room.
        Args:
            room (Room): Room instance to exit.
        """
        room.clear_room(True)

        if room.room_type == "Boss":
            self.gui.exit_boss_room()
            self.total_enemies_killed += 1
        elif room.room_type == "Combat":
            self.total_enemies_killed += room.enemies_killed
            self.gui.exit_combat_room(room)
        else:
            self.gui.exit_room(room)

    def end_game(self, is_game_won: bool):
        """Ends the game and display corresponding GUI.
        Args:
            is_game_won (bool): If the game has been won or lost.
        """

        # Display to player total time spent
        total_time = math.trunc(time.time() - self.initial_time)

        if is_game_won:
            self.gui.display_game_won_gui(total_time,
                                          self.total_enemies_killed,
                                          self.total_rooms_entered)
        else:
            self.gui.display_game_lost_gui(total_time,
                                           self.total_enemies_killed,
                                           self.total_rooms_entered)

    def save_game(self):
        """Saves current game data to a save file.
        """
        self.save_manager.write_to_save_file(
            {
                "Round_Number": self.counter,
                "Map": self.map,
                "Player": self.player,
                "sessions_stats": {
                    "timestamp": datetime.datetime.now(),
                    "enemies_killed": self.total_enemies_killed,
                    "rooms_entered": self.total_rooms_entered
                }
            }
        )

    def load_game(self):
        """Loads save file data from an existing save file.
        """
        content = self.save_manager.get_save()
        print(content)

        print(f"Player Health: {content['Player'].stats['Health']}")
        self.start_from_save(content)

    def clear_save_file(self):
        """Clears previous save data.
        """
        self.save_manager.clear_save_file()

    def is_save_empty(self):
        """Checks if the save is empty.
        """
        return self.save_manager.is_save_empty()
