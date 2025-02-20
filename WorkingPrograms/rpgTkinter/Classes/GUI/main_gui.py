"""Module containing the MainGUI class.
"""

from functools import partial
import tkinter as tk
import customtkinter
from PIL import ImageTk, Image
from Classes.GUI.button import Button
from Classes.GUI.character_gui import CharacterGUI
from Classes.GUI.inventory_gui import InventoryGUI
from Classes.text_printer import TextPrinter


class MainGUI(tk.Tk):
    """Class involving the main game window.
    """

    # Default size of the window.
    def __init__(self, player, game_handler):
        """Creates the instance.
        Args:
            player: The player instance
            game_handler: The game_handler instance.
        """
        super().__init__()
        self.title("Spaceship Game")
        self.geometry('1300x900')  # Window size is provided by user.
        self.resizable(False, False)
        self.minsize(800, 500)  # Minimum size of the window, can be maximized.
        self.iconbitmap('Images/LevelOne/SpaceShip.ico')
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.screen_width = 1300
        self.screen_height = 900
        self.player = player
        self.game_handler = game_handler
        self.game_handler.set_gui(self)
        self.ready = True
        self.bg = None
        self.bg_canvas = None
        self.is_game_started = False

        # self.create_intro_screen1()
        self.create_main_screen()
        self.mainloop()

    def createText(self, msg: str, x: int, y: int,
                   font: tuple[str, int] = ("Time New Romans", 20),
                   color: str = 'black', anchor: str = "center",
                   tags: str = None, width: int = None, shadow: bool = False,
                   justify="left"):
        """Creates text using custom formatting
        Args:
            msg: The message to print
            x: The x-location
            y: The y-position
            font: The font style and size
            color: The font color
            anchor: Where to anchor the text to
            tags: The tag string to refer it by
            width: The width of the textbox
            shadow: Whether to have a background shadow or not
            justify: How to align the text

        """
        if shadow:
            self.bg_canvas.create_text(x-5, y+5, text=msg, font=font,
                                       fill="black", anchor=anchor, tags=tags,
                                       width=width)
        self.bg_canvas.create_text(x, y, text=msg, font=font, fill=color,
                                   anchor=anchor, tags=tags, width=width,
                                   justify=justify)

    def clearGUI(self, img):
        """Clears the gui of existing elements
        Args:
            img: The image to replace the destroyed screen by
        """
        if self.bg_canvas is not None:
            self.bg_canvas.destroy()
        self.bg_canvas = tk.Canvas(self, width=self.screen_width,
                                   height=self.screen_height)
        self.bg_canvas.pack(fill='both', expand=True)
        self.img = Image.open(img).resize((self.screen_width,
                                           self.screen_height))
        self.image = ImageTk.PhotoImage(self.img)
        self.bg_canvas.create_image(0, 0, image=self.image, anchor='nw')

    def create_main_screen(self):
        """Creates the main screen graphics.
        """
        self.clearGUI("Images/download.jpg")

        self.createText("Space Adventure RPG", self.screen_width//2, 200,
                        font=("Arial", 80), color="white")

        Button(self, "New Game", self.create_intro_screen1,
               self.screen_width//2 - 100, 500, font=("Arial", 40),
               hcolor="#ff6700", width=250)

        if not self.game_handler.is_save_empty():
            Button(self, "Load Game", self.load_game,
                   self.screen_width//2 - 100, 600, font=("Arial", 40),
                   hcolor="#FF00FF", width=250, tags="load")

    def load_game(self):
        """Loads the game from the save file.
        """
        self.game_handler.load_game()

    def save_game(self):
        """Saves current game data to a save file.
        """
        self.game_handler.save_game()

    def create_intro_screen1(self):
        """Creates the title screen."""

        # Delete save file
        self.game_handler.clear_save_file()

        self.game_handler.clear_save_file()
        self.clearGUI('Images/LevelOne/bg2.jpeg')
        self.createText("Are You Ready For a New Adventure?",
                        self.screen_width // 2, self.screen_height // 2,
                        font="Time_New_Roman 45", color='white', shadow=True)
        self.user_name = tk.Label(self, text='User Name:',
                                  font='Time_New_Roman 15')
        self.user_name_window = self.bg_canvas.create_window(30, 100,
                                                             anchor='sw',
                                                             window=self.user_name, tags="Login_Text")
        self.user_name_entry = tk.Entry(self, font='Time_New_Roman 20')
        self.bg_canvas.create_window(150, 100, anchor='sw',
                                     window=self.user_name_entry,
                                     tags="Login Button")

        Button(self, "Start Game", self.create_intro_screen2, 30, 200)
        Button(self, "Exit", self.destroy, self.width-200, self.height-100,
               font=("Times", 30))

    def create_intro_screen2(self):
        """Destroys the title screen and Creates the game intro screen."""
        self.clearGUI('Images/LevelOne/bg.jpg')
        self.name = self.user_name_entry.get() or "Default"
        self.player.change_name(self.name)
        self.createText(
            "You are a new  Space Janitor sent to"
            " salvage the numerous asteroids and ship"
            " wrecks that pollute space."
            f"\n\nWelcome, {self.name} to being a"
            f" Space Janitor.\nRise to the top.",
            self.width//2, self.height-700, font=("Times New Romans", 20),
            color="white", shadow=True
        )
        Button(self, "Click Here to Continue", self.create_intro_screen3,
               self.width//2, self.height-300, anchor="center")

    def printPlayerStats(self):
        """Prints player stats.
        """
        self.bg_canvas.delete("stats")
        self.createText(
            f"{self.player.name}'s Stats:\n\nHealth:"
            f"{self.player.stats['Health']}/{self.player.stats['Max Health']}"
            + "".join([f'\n\n{stat[0:3]}: {self.player.stats[stat]}'
                       for stat in ["Strength", "Dexterity",
                                    "Vitality", "Intelligence"]]) +
            f"\n\nFree Points: {self.player.stats['Stat Points']}\n\n"
            f"Min: 3, Max: 12",
            self.width//2, self.height - 600,
            font=("Time New Romans", 22), color="white", justify="center",
            tags="stats"
        )

    def update_init_stats(self, stat: str, amount: int):
        """Method that affects the Player's stats.
        Args:
            stat (str): The stat to change.
            amount (int): How much to change the stat by.
             Increases only if the Player has unassigned Stat Points.
        """
        if amount == -1:
            if self.player.stats[stat] > 3:
                self.player.stats[stat] += amount
                self.player.stats["Stat Points"] += -amount
        elif self.player.stats["Stat Points"] >= 1:
            if self.player.stats[stat] < 12:
                self.player.upgrade_stats(stat, amount)
        self.player.update_max_health()
        self.player.stats["Health"] = self.player.stats["Max Health"]
        self.printPlayerStats()

    def create_intro_screen3(self):
        """Creates the character creation screen after deleting the intro
         screen text."""
        self.clearGUI('Images/LevelOne/bg.jpg')
        Button(self, "Start Game", self.create_main_gui, self.width//2,
               self.height-300, anchor="center")
        self.printPlayerStats()

        for i, stat in enumerate(["Strength", "Dexterity",
                                  "Vitality", "Intelligence"]):
            cmd = lambda s, n: lambda: self.update_init_stats(s, n)

            Button(self, "-", cmd(stat, -1), self.width//2 + 70,
                   self.height - 700 + 70 * i,
                   width=1, height=1, font=("Time New Romans", 20),
                   anchor="center", padding=5)
            Button(self, "+", cmd(stat, 1), self.width//2 + 100,
                   self.height - 700 + 70 * i,
                   width=1, height=1, font=("Time New Romans", 20),
                   anchor="center", padding=5)

    def create_main_gui(self):
        """Deletes the character screen and makes the main screen.
        """
        self.start_game()
        from Classes.game_handler import GameHandler
        # To import the Level counter from GameHandler
        self.lvl_counter = GameHandler.counter
        self.is_game_started = True

        self.clearGUI('Images/LevelOne/HallWay.png')

        menu_image = Image.open('Images/LevelOne/info_bg.png').resize((350,
                                                                       210))
        self.menu_bg = ImageTk.PhotoImage(menu_image)

        self.image_border = Image.open('Images/Items/Button_image.png').resize((650, 270))
        self.border = ImageTk.PhotoImage(self.image_border)

        if self.lvl_counter == 1:

            self.original_image = Image.open('Images/LevelOneMap/Main.jpg').resize((400, 500))
            self.bg = ImageTk.PhotoImage(self.original_image)

        elif self.lvl_counter == 2:
            self.original_image = Image.open('Images/LevelTwoMap/Level2.jpg').resize((400, 500))
            self.bg = ImageTk.PhotoImage(self.original_image)

        elif self.lvl_counter == 3:
            self.original_image = Image.open('Images/Level3/LevelThreeMap/Level_3.jpg').resize((400, 500))
            self.bg = ImageTk.PhotoImage(self.original_image)

        # Create Canvas and Images
        self.bg_canvas.create_image(self.screen_width - 1280,
                                    self.screen_width - 1280,
                                    image=self.bg, anchor='nw')
        self.bg_canvas.create_image(self.screen_width - 1400,
                                    self.screen_height - 360,
                                    image=self.border, anchor='nw')
        self.bg_canvas.create_image(self.screen_width - 1250,
                                    self.screen_height - 330,
                                    image=self.menu_bg, anchor='nw')
        self.createText(f"{self.name}'s Stats", 120, 590, font=("Time_New_Roman", 20, "bold"),
                        color="white", anchor="w")

        Button(self, "Character\nDetails", self.open_character_gui,
               self.screen_width - 1210, self.screen_height - 275, anchor="nw",
               width=50, color="#faa19b", hcolor="#f06b62")
        Button(self, "Inventory\nDetails", self.open_inventory_gui,
               self.screen_width - 1060, self.screen_height - 275, anchor="nw",
               width=50, color="#faa19b", hcolor="#f06b62")
        Button(self, "Exit", self.destroy, 20, self.screen_height - 50,
               anchor="w", font=("Calibri", 20))

        self.createText("\nYou are ready to start cleaning up"
                        " the wreckage. Which wreckage should you"
                        " visit first? Choose a location on the map.\n",
                        450, 350, font=("Times New Roman", 17), color="white",
                        anchor="w", tags="game_text", width=500)
        self.createText("Choose Next Location", 1010, 400, font=("Time_New_Roman", 20),
                        color="white", anchor="w")

        # Button(self, "Load Game", self.load_game, self.screen_width - 180, 80,
        #        font=("Arial", 20))
        # Button(self, "Save Game", self.save_game, self.screen_width - 180, 130,
        #        font=("Arial", 20))

        self.display_buttons()

    def start_game(self):
        """Start the game and load available rooms.
        """
        self.text_printer = TextPrinter(self)
        self.ready = True
        self.map = self.game_handler.get_map()
        self.player = self.game_handler.player
        self.name = self.game_handler.player.name
        self.game_handler.enter_room(self.map.get_current_room())

    def display_buttons(self):
        """Display available rooms to interact with.
        """
        self.button_frame = tk.Frame(self.bg_canvas, bg='#023552',
                                     borderwidth=3, highlightcolor="white",
                                     highlightthickness=4)
        self.button_frame.place(relwidth=0.20, relheight=0.4,
                                relx=0.77, rely=0.5)

        self.button_image = Image.open('Images/Items/Button_image.png').resize((500, 450))
        self.button_background = ImageTk.PhotoImage(self.button_image)
        self.bg_canvas.create_image(self.width - 420, self.height - 495, image=self.button_background,
                                    anchor='nw')

        for adjacent_room in self.map.get_current_room().get_adjacent_rooms():
            test = lambda room: lambda: self.handle_button_input(room)
            button_text = adjacent_room.name

            color = "#f69697" if adjacent_room.cleared else "#FFFFFF"

            button = customtkinter.CTkButton(
                self.button_frame, width=200, height=3, font=("Calibri", 15),
                text_color="black", text=button_text,
                command=test(adjacent_room), fg_color=color
            )
            button.pack(pady=5)

    def handle_button_input(self, room):
        """Enters the Room instance and changes the map image to the
         appropriate one.
        Args:
            room (Room): The Room instance just entered.
        """
        if self.ready and self.player.living and self.map.current_room.cleared:
            self.change_map_image(room)
            self.game_handler.enter_room(room)

    def change_map_image(self, room):
        """Changes the minimap to the new image.
        Args:
            room (Room): The Room instance with the associated image.
        """
        self.original_image = Image.open(room.map_image_path).resize((400,
                                                                      500))
        self.bg = ImageTk.PhotoImage(self.original_image)
        self.bg_canvas.create_image(self.screen_width - 1280,
                                    self.screen_width - 1280, image=self.bg,
                                    anchor='nw')

    def animate_text(self, text_id, text):
        """Prints text to the MainGUI
    .
        Args:
            text_id (str): The text_box to print to.
            text (str): The text to print.
        """
        self.text_printer.animate_text(text, text_id, tk.END)

    def enter_repeated_room(self, room):
        """Prints text when entering a previously cleared room.
        Args:
            room (Room): The already cleared room.
        """
        self.text_printer.animate_text(f"\n{room} has already been entered.\n",
                                       "game_text", tk.END)

    def enter_chest_room(self, room):
        """Prints text when entering a ChestRoom.
        Args:
            room (ChestRoom): The ChestRoom instance to enter.
        """
        self.text_printer.animate_text(f"\nYou have entered {room} which"
                                       f" contains a chest.\n", "game_text",
                                       tk.END)

    def enter_shop_room(self, room):
        """Prints text when entering a ShopRoom.
        Args:
            room (ShopRoom): The ShopRoom instance to enter.
        """
        self.text_printer.animate_text(f"\nYou have entered {room} which"
                                       f" contains a shop.\n", "game_text",
                                       tk.END)

    def enter_combat_room(self, room):
        """Prints text when entering a CombatRoom.
        Args:
            room (CombatRoom): The CombatRoom instance to enter.
        """
        self.text_printer.animate_text(f"\nYou have entered {room} which"
                                       f" contains combat.\n", "game_text",
                                       tk.END)

    def enter_boss_room(self, room):
        """Prints text when entering a BossRoom.
        Args:
            room (BossRoom): The BossRoom instance to enter.
        """
        self.text_printer.animate_text(f"\n You have entered {room} which is"
                                       f" the boss room.\n", "game_text",
                                       tk.END)

    def exit_boss_room(self):
        """Prints text when exiting a BossRoom.
        """
        if not self.player.living:
            return

        self.text_printer.animate_text("\nCongratulations for beating the"
                                       " boss!\n", "game_text", tk.END)

        # Display End Game Button
        Button(self, "End Game", partial(self.game_handler.end_game, True),
               self.width-100, 300, anchor="e", width=10, font=("Calibri", 16),
               height=2)

        # Display Text
        self.bg_canvas.create_text(1010, 235, width=300, font=('Arial', 20),
                                   fill="#FFFFFF", anchor="w",
                                   text="Move to Next Round")

    def exit_room(self, room):
        """Prints text when exiting a Room.
        Args:
            room (Room): The Room instance that was just cleared.
        """
        self.text_printer.animate_text(f"\nYou have exited {room}.\n",
                                       "game_text", tk.END)

    def exit_combat_room(self, room):
        """Prints text when exiting a CombatRoom.
        Args:
            room (CombatRoom): The CombatRoom instance that was just cleared.
        """
        if self.player.living:
            self.text_printer.animate_text(f"\nYou have beaten the enemies"
                                           f" in {room}.\n", "game_text",
                                           tk.END)
        else:
            self.game_handler.end_game(False)

    def open_inventory_gui(self):
        """Opens an InventoryGUI instance.
        """
        if (self.ready and self.map.get_current_room().get_cleared()
                and self.player.living):
            self.ready = False
            self.map.get_current_room().clear_room(False)
            InventoryGUI(self.player, self.map.get_current_room(), self)

    def open_character_gui(self):
        """Opens a CharacterGUI instance.
        """
        print("clicking character")
        print(f"ready: {self.ready}, current:"
              f" {self.map.get_current_room().get_cleared()}")
        print(f"living: {self.player.living}")
        if (self.ready and self.map.get_current_room().get_cleared()
                and self.player.living):
            self.ready = False
            self.map.get_current_room().clear_room(False)
            CharacterGUI(self.player, self.map.get_current_room(), self)

    def display_game_lost_gui(self, total_time, enemies_killed, rooms_entered):
        """The screen that shows when you lose the game.
        Args:
            total_time (int): The total time spent.
            enemies_killed (int): The number of enemies killed.
            rooms_entered (int): The number of rooms entered.
        """

        # Clear previous window
        self.bg_canvas.destroy()

        # Import Map Background
        img = Image.open('Images/LevelOne/GameOver.png').resize((self.screen_width, self.screen_height))
        self.img = ImageTk.PhotoImage(img)

        # Create canvas and background
        self.bg_canvas = tk.Canvas(self, width=self.screen_width,
                                   height=self.screen_height)
        self.bg_canvas.pack(fill='both', expand=True)
        self.bg_canvas.create_image(0, 0, image=self.img, anchor='nw')

        # Heading
        self.bg_canvas.create_text(self.width / 2, self.height / 5 - 100,
                                   font=('Calibri', 50), fill="#ffffff",
                                   justify="center", text="You have died!")
        # Subheading
        self.bg_canvas.create_text(self.width / 2, self.height / 5,
                                   font=('Calibri', 35), fill="#ffffff",
                                   justify="center",
                                   text="You have failed to eradicate all the"
                                   " monsters in the wreckages.")

        # Final stats
        self.bg_canvas.create_text(300, self.height / 4 + 275,
                                   font=('Calibri', 25), fill="#ffffff",
                                   justify="left",
                                   text=f'{self.player.name}\'s Stats:\n\n' +
                                        f'Total Time (s): {total_time}.\n' +
                                        f'Enemies Slain: {enemies_killed}.\n' +
                                        f'Rooms Entered: {rooms_entered}.\n' +
                                        f'Max Health: '
                                        f'{self.player.stats["Max Health"]}.\n'
                                        + f'Strength:'
                                        f' {self.player.stats["Strength"]}.\n'
                                        + f'Dexterity:'
                                        f' {self.player.stats["Dexterity"]}.\n'
                                        + f'Vitality:'
                                        f' {self.player.stats["Vitality"]}.\n'
                                        + f'Intelligence: '
                                        f'{self.player.stats["Intelligence"]}.'
                                   )

        Button(self, "Retry?", self.game_handler.start_new_game, 700,
               self.screen_height//2, anchor="nw", width=8, height=3,
               font=("Calibri", 20))
        Button(self, "Exit", self.destroy, 550, self.screen_height//2,
               anchor="w", width=8, height=3, font=("Calibri", 20))

        print(f"save is: {self.game_handler.is_save_empty}")
        if not self.game_handler.is_save_empty:
            Button(self, "Reload from Save",self.load_game, 550,
                   self.screen_height//2, 800, anchor="w", width = 15,
                   height = 3, font=("Calibri", 20))

    def display_game_won_gui(self, total_time, enemies_killed, rooms_entered):
        """The screen that shows when you win the game.
        Args:
            total_time (ChestRoom): The ChestRoom instance to enter.
            enemies_killed (int): The number of enemies killed.
            rooms_entered (int): The number of rooms entered.
        """
        # Clear previous window
        self.bg_canvas.destroy()

        # Import Map Background
        img = Image.open('Images/LevelOne/GameWon.png').resize(
            (self.screen_width, self.screen_height))
        self.img = ImageTk.PhotoImage(img)

        # Create canvas and background
        self.bg_canvas = tk.Canvas(self, width=self.screen_width,
                                   height=self.screen_height)
        self.bg_canvas.pack(fill='both', expand=True)
        self.bg_canvas.create_image(0, 0, image=self.img, anchor='nw')

        # Heading
        self.bg_canvas.create_text(self.width / 2, self.height / 5 - 100,
                                   font=('Calibri', 50), fill="#ffffff",
                                   justify="center", text="You have won!")
        # Subheading
        self.bg_canvas.create_text(self.width / 2, self.height / 5,
                                   font=('Calibri', 30), fill="#ffffff",
                                   justify="center",
                                   text="You have successfully eradicated all"
                                   " the monsters in the wreckages.")

        # Final stats
        self.bg_canvas.create_text(300, self.height / 4 + 275,
                                   font=('Calibri', 25), fill="#ffffff",
                                   justify="left",
                                   text=f'{self.player.name}\'s Stats:\n\n' +
                                        f'Total Time (s): {total_time}.\n' +
                                        f'Enemies Slain: {enemies_killed}.\n'
                                        + f'Rooms Entered: {rooms_entered}.\n'
                                        + f'Max Health: '
                                        f'{self.player.stats["Max Health"]}.\n'
                                        + f'Strength:'
                                        f' {self.player.stats["Strength"]}.\n'
                                        + f'Dexterity:'
                                        f' {self.player.stats["Dexterity"]}.\n'
                                        + f'Vitality:'
                                        f' {self.player.stats["Vitality"]}.\n'
                                        + f'Intelligence: '
                                        f'{self.player.stats["Intelligence"]}.'
                                   )

        Button(self, "Continue", self.game_handler.start_next_map, 700,
               self.screen_height//2, anchor="nw", width=8, height=3,
               font=("Calibri", 20))
        Button(self, "Exit", self.destroy, 550, self.screen_height//2,

               anchor="w", width=8, height=3, font=("Calibri", 20))

    def destroy(self):
        if self.is_game_started and self.player.living and not self.player.is_in_combat:
            self.game_handler.save_game()
        super().destroy()
