"""Module for the StartRoom class.
"""
from Classes.Rooms.room import Room


class StartRoom(Room):
    """The initial starting room.
    """
    def __init__(self):
        """Creates the instance."""
        super().__init__()
        self.name = "Start"
        self.room_type = "Start"
        self.text = "You are in the start room."
