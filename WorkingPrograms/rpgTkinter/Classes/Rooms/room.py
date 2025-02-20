"""Module for the parent Room class.
"""

import csv
import random


class Room:
    """Parent class for more specialized rooms.
    """
    def __init__(self):
        """Creates the instance.
        """
        self.adjacent_rooms = []
        self.is_currently_entered = False
        self.has_entered = False
        self.cleared = False
        self.name = None
        self.map_image_path = None

        self.edges = []
        self.pos_x = None
        self.pos_y = None

    def set_coordinates(self, pos_x, pos_y):
        """Setter for the room coordinates.
        Args:
            pos_x (int): The X coordinate.
            pos_y (int): The Y coordinate.
        """
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_coordinates(self):
        """Getter for the room's coordinates.
        Returns:
            list[int, int]: The room's coordinates in the format [x, y].
        """
        return [self.pos_x, self.pos_y]

    def clear_room(self, status: bool):
        """Setter for the room's cleared status.
        Args:
            status (bool): Whether the room is cleared or not.
        """
        self.cleared = status

    def get_cleared(self):
        """Getter for the room's cleared status.
        Returns:
            cleared (bool): The room's cleared status.
        """
        return self.cleared

    def set_image_path(self, path):
        """Setter for the room's image.
        Args:
            path (str): The file path for the image.
        """
        self.map_image_path = path

    def create_adjacency(self, other_room):
        """Makes this room adjacent to another room and vice versa.
        Args:
            other_room (Room): The other room.
        """
        if other_room not in self.adjacent_rooms:
            self.adjacent_rooms.append(other_room)
        if self not in other_room.get_adjacent_rooms():
            other_room.add_adjacent_room(self)

    def add_adjacent_room(self, other_room):
        """Makes another room adjacent to this room but not vice versa.
        Args:
            other_room (Room): The other room.
        """
        self.adjacent_rooms.append(other_room)

    def get_adjacent_rooms(self):
        """Getter for the list of rooms adjacent to this one.
        Returns:
            adjacentRooms (list): The list of adjacent Room isntances.
        """
        return self.adjacent_rooms

    def generate_name(self, room_type):
        """Setter for the room's name based on its type.
        Args:
            room_type (str): The room's type. "Chest", "Boss", "Combat",
             "Shop", or "Start".
        Return:
            name (str): The name of the room.
        """

        from Classes.game_handler import GameHandler
        # To import the Level counter from GameHandler
        self.lvl_counter = GameHandler.counter

        level_1 = []
        level_2 = []
        level_3 = []

        names = []
        with open(f'Names/{room_type}RoomNames.txt',
                  'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                names.extend(row)

        level_1 = names[:23]  # There are 23 Rooms for Level 1

        if len(names) < 10:  # Adds the chest rooms to the list.
            level_2 = level_1
            level_3 = level_1

        else:
            level_2 = names[23:47]
            level_3 = names[47:]

        if self.lvl_counter == 1:
            self.name = random.choice(level_1)

        elif self.lvl_counter == 2:
            self.name = random.choice(level_2)

        elif self.lvl_counter == 3:
            self.name = random.choice(level_3)
        return self.name

    def __repr__(self):
        """Representation of the room.
        Returns:
            name (str): The name of the room.
        """
        return self.name

    def __eq__(self, other):
        """Checks whether two rooms are overlapping.
        Args:
            other (Room): The room being compared.
        Returns:
            bool: True if the room's X- and Y-coordinates are the same.
        """
        return self.pos_x == other.pos_x and self.pos_y == other.pos_y
