"""Module for the CharacterGUI class.
"""


import tkinter as tk
from PIL import ImageTk, Image
from Classes.GUI.button import Button
from Classes.character import Player
from Classes.Rooms.room import Room


class CharacterGUI(tk.Toplevel):
    """Class governing all player-game interactions involving
     the Character's stats.
    """
    def __init__(self, player: Player, room: Room, gui):
        """Creates the instance.
        Args:
            player (Player): The Player instance to interact with.
            room (Room): The current room the Player is in.
            gui: The parent gui.
        """

        super().__init__()
        self.title("Character Screen")
        self.geometry(f'{400}x{600}+400+50')
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.minsize(self.width, self.height)  # Min size, can be maximized.
        self.iconbitmap('Images/LevelOne/SpaceShip.ico')
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.player = player
        self.room = room
        self.gui = gui

        # Customize screen
        self.original_image = Image.open('Images/LevelOne/Stats.jpg').resize((self.width, self.height))
        self.bg = ImageTk.PhotoImage(self.original_image)

        self.bg_canvas = tk.Canvas(self, width=self.width, height=self.height,
                                   bg="#043F5B")
        self.bg_canvas.pack(fill='both', expand=True)
        self.bg_canvas.create_image(0, 0, image=self.bg, anchor='nw')

        Button(self, "Close", self.destroy, int(self.width / 2 + 40), self.height - 30,
               font=("Cambria", 20, "bold"))

        self.update_character_gui()

        self.mainloop()

    def stat_button(self, stat: str, amount: int):
        """Method governing what happens when a stat-increase button
         is pressed.
        Args:
            stat (str): The stat to be affected.
            amount (int): How much to increase the stat by.
        """
        if self.player.stats["Stat Points"] > 0:
            self.player.upgrade_stats(stat, amount)
            if stat == "Vitality":
                self.player.update_max_health()
                self.player.stats["Health"] += 5
                self.player.update_max_health()
                self.player.update_defense()
            if stat == "Strength":
                self.player.update_attack()
        self.update_character_gui()

    def level_up(self):
        """Method to increase the player's level when the button is clicked.
        """
        if self.player.stats["XP"] >= self.player.stats["Level"] * 10:
            self.player.lv_up()
        if self.player.stats["XP"] < self.player.stats["Level"] * 10:
            self.bg_canvas.delete("level_up")
        self.update_character_gui()

    def update_character_gui(self):
        """Method to update the display whenever a button is clicked.
        """
        # pylint: disable=W0108

        self.bg_canvas.delete("stats")
        self.bg_canvas.delete("button")
        self.bg_canvas.delete("level_up")

        self.bg_canvas.create_text(
            self.width/2 - 50, self.height - 300,
            text=f"{self.player.name}'s Stats:\n\nHealth:" +
            f"\n{self.player.stats['Health']}/"
            f"{self.player.stats['Max Health']}" +
            "".join([f'\n\n{stat[0:3]}: {self.player.stats[stat]}' for stat in
                     ["Strength", "Dexterity", "Vitality", "Intelligence"]]) +
            f"\n\nFree Points: {self.player.stats['Stat Points']}" +
            f"\nLevel: {self.player.stats['Level']}" +
            f"\nXP: {self.player.stats['XP']}/"
            f"{self.player.stats['Level'] * 10}",
            font=("Cambria", 18, "bold"), fill="#FFFFFF", justify="center",
            tags="stats"
        )

        if self.player.stats["Stat Points"] > 0:
            for i, stat in enumerate(["Strength", "Dexterity",
                                      "Vitality", "Intelligence"]):
                cmd = lambda s, n: lambda: self.stat_button(s, 1)

                Button(self, "+", cmd(stat, 1), int(self.width / 2 + 60),
                       self.height - 360 + 50 * i,
                       width=1, height=1, font=("Time New Romans", 20),
                       anchor="center", tags="button")

        if self.player.stats["XP"] >= self.player.stats["Level"] * 10:
            Button(self, "LV Up", lambda: self.level_up(),
                   self.width // 2 + 140, self.height - 360 + 250,
                   width=1, height=1, font=("Cambria", 20, "bold"),
                   anchor="center", tags="level_up")

    def destroy(self):
        """Method governing what happens when the window is destroyed.
        """
        self.room.clear_room(True)
        self.gui.ready = True
        super().destroy()
