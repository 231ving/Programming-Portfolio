"""Module containing the FightGUI class.
"""

import random
import tkinter as tk
from functools import partial
from PIL import ImageTk, Image
from Classes.GUI.button import Button
from Classes.character import Player, Enemy, Character
from Classes.Rooms.combat_room import CombatRoom


class FightGUI(tk.Toplevel):
    """Class governing player-system interactions during an active FightRoom.
    """
    def __init__(self, room: CombatRoom, player: Player, game_handler):
        """Creates the instance.
        Args:
            room (CombatRoom): The CombatRoom instance.
            player (Player): The Player instance being controlled.
            game_handler: The gameHandler instance.
        """

        super().__init__()
        # To import the Level counter from GameHandler
        from Classes.game_handler import GameHandler

        self.title("Combat Screen")
        self.geometry(f'{1000}x{800}+150+50')
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.minsize(self.width, self.height)  # Min size, can be maximized.
        self.iconbitmap('Images/LevelOne/SpaceShip.ico')
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.player = player
        self.player.is_in_combat = True
        self.room = room
        self.enemies = room.enemies
        self.room_name = room.__repr__()
        self.game_handler = game_handler
        self.no_enemy = False
        self.enemies_txt = ""
        self.count = 0
        self.enemy_entry = None
        self.exit_button = None
        self.turn_counter = 0
        self.player_txt1 = ""
        self.player_txt2 = ""
        self.enemy_txt1 = ""
        self.enemy_txt2 = ""
        self.lvl_counter = GameHandler.counter

        self.rooms = {
            'Weapons Bay': '#95F21C', 'Main Cabin': '#95F21C', 'Elevator 1': '#D18A00',
            'Storage Area': '#95F21C', 'Kitchen': '#D18A00', 'Barracks': '#D18A00', 
            'Cafeteria': '#54B851', 'Life Pod 1': '#95F21C', 'Cabin 2': '#54B851',
            'Showers': '#95F21C', 'Cabin 1': '#BE0000', 'Docking Port': '#95F21C', 
            'Bridge': '#95F21C', 'Elevator 3': '#95F21C', 'Elevator 2': '#D18A00',
            'Cabin 3': '#95F21C', 'Captains Cabin': '#D18A00', 'Hangar': '#FFF000', 
            'Life Pod 2': '#95F21C', 'Engine Room': '#95F21C', 'Pod Bay': '#54B851',
            'Life Pod 3': '#00FFFC', 'Bathroom': '#95F21C'
        }
        self.simple_colors = ['#FAFF00', '#FDD800', '#ACFF42', '#FFFFFF']

        if self.lvl_counter == 1:
            self.text_color = self.rooms.get(self.room_name)
            self.original_image = Image.open('Images/LevelOne/' + self.room_name
                                             + '.jpg').resize((self.width, self.height))
            self.bg = ImageTk.PhotoImage(self.original_image)
        elif self.lvl_counter == 2:
            self.text_color = random.choice(self.simple_colors)
            self.original_image = Image.open('Images/LevelTwo/' + self.room_name
                                             + '.jpg').resize((self.width, self.height))
            self.bg = ImageTk.PhotoImage(self.original_image)

        elif self.lvl_counter == 3:
            self.text_color = random.choice(self.simple_colors)
            self.original_image = Image.open('Images/Level3/LevelThree/' + self.room_name
                                             + '.jpg').resize((self.width, self.height))
            self.bg = ImageTk.PhotoImage(self.original_image)

        # Stats images and image name box.
        self.health_icon = Image.open('Images/Items/Health.png').resize((30, 30))
        self.health_stat_icon = ImageTk.PhotoImage(self.health_icon)

        self.attack_icon = Image.open('Images/Items/Attack.png').resize((30, 30))
        self.att_stat_icon = ImageTk.PhotoImage(self.attack_icon)

        self.def_icon = Image.open('Images/Items/defense.png').resize((30, 30))
        self.deff_stat_icon = ImageTk.PhotoImage(self.def_icon)

        self.med_image = Image.open('Images/Items/Medkit.png').resize((30, 30))
        self.med_kit_image = ImageTk.PhotoImage(self.med_image)

        self.name_b = Image.open('Images/Items/name_bar.png').resize((300, 80))
        self.name_box = ImageTk.PhotoImage(self.name_b)

        self.enemy_name_bx = self.name_box

        self.bg_canvas = tk.Canvas(self, width=self.width, height=self.height,
                                   bg="#043F5B")
        self.bg_canvas.pack(fill='both', expand=True)
        self.bg_canvas.create_image(0, 0, image=self.bg, anchor='nw')

        self.bg_canvas.create_image(30, self.height - 800, image=self.name_box, anchor='nw')
        self.bg_canvas.create_image(self.width / 2 + 170, self.height - 800, image=self.name_box, anchor='nw')

        self.bg_canvas.create_text(self.width / 2 - 350, self.height - 760,
                                   font="Cambria_Math 15 bold",
                                   fill=self.text_color, justify="center",
                                   text=self.player.name + "'s Side",
                                   tags="equipment_title")

        self.bg_canvas.create_text(self.width / 2 - 65, self.height - 760,
                                   font="Cambria_Math 15 bold",
                                   fill=self.text_color, justify="center",
                                   text="Ship #" + str(self.lvl_counter),
                                   tags="lvl")

        t = "Enemies' Side" if not self.room.is_boss_room else "Boss Side"
        self.bg_canvas.create_text(self.width / 2 + 350, self.height - 760,
                                   font="Cambria_Math 15 bold",
                                   fill=self.text_color, justify="center",
                                   text=t, tags="Enemies")

        self.bg_canvas.create_image(50, self.height - 360, image=self.health_stat_icon, anchor='nw')
        self.bg_canvas.create_image(50, self.height - 325, image=self.att_stat_icon, anchor='nw')
        self.bg_canvas.create_image(50, self.height - 290, image=self.deff_stat_icon, anchor='nw')
        self.bg_canvas.create_image(50, self.height - 260, image=self.med_kit_image, anchor='nw')

        # "Partial" binds a parameter to the function, another way to do this
        # without a lambda expression
        Button(self, "Defend", partial(self.defend, self.player), 50, 780,
               font=("Cambria Math", 12, "bold"), tags="defend_button")
        Button(self, "Use Medkit", self.use_medkit, 200, 780,
               font=("Cambria Math", 12, "bold"))

        for enemy in self.enemies:
            self.set_enemy_actions(enemy)
        self.combat_log()

        self.update_combat_gui()
        self.mainloop()

    def player_grid(self):
        """Creates and updates the player's side of the display.
        """
        self.bg_canvas.delete("health", "attack", "defense", "medkits")
        self.bg_canvas.create_text(90, self.height - 330, anchor='sw',
                                   font="Cambria_Math 15 bold",
                                   fill=self.text_color, justify="center",
                                   text="Health:\t"
                                   + str(self.player.stats["Health"]) + " / "
                                   + str(self.player.stats["Max Health"]),
                                   tags="health")
        self.bg_canvas.create_text(90, self.height - 300, anchor='sw',
                                   font="Cambria_Math 15 bold",
                                   fill=self.text_color, justify="center",
                                   text="Attack:\t" + str(self.player.attack),
                                   tags="ff0d1d")
        self.bg_canvas.create_text(90, self.height - 270, anchor='sw',
                                   font="Cambria_Math 15 bold",
                                   fill=self.text_color, justify="center",
                                   text="Defense:\t" + str(self.player.defense),
                                   tags="defense")
        self.bg_canvas.create_text(90, self.height - 240,
                                   anchor='sw', font="Cambria_Math 15 bold",
                                   fill=self.text_color,
                                   justify="center", tags="medkits",
                                   text="Medkits: "
                                   + str(self.player.stats["Medkits"]))

    def update_combat_gui(self):
        """Calls all parts of the GUI display and updates it.
        """
        self.player_grid()
        self.attack_buttons()
        self.enemy_grid()
        self.make_exit()

    def enemy_grid(self):
        """Creates and updates the display for all enemies.
        """
        # To import the Level counter from GameHandler
        from Classes.game_handler import GameHandler
        self.lvl_counter = GameHandler.counter

        self.bg_canvas.delete("enemies")
        self.enemies_txt = ""
        self.count = 0
        if len(self.enemies) > 0:
            for enemy in self.enemies:
                self.enemies_txt += ("\n" + str(self.count) + ") "
                                     + str(enemy.name) + "\n  "
                                     + "LV: " + str(enemy.stats["Level"])
                                     + " | Health: "
                                     + str(enemy.stats["Health"]) + "\n  "
                                     + str(enemy.get_attack()) + " Damage | "
                                     + str(enemy.get_defense()) + " Defense\n\n")
                self.count += 1
        else:
            self.enemies_txt = "No Enemies Remain"
        self.bg_canvas.create_text(self.width / 2 + 350, self.height - 600,
                                   font="Cambria_Math 12 bold",
                                   fill=self.text_color, justify="center",
                                   text=self.enemies_txt, tags="enemies", anchor="n")

    def attack_buttons(self):
        """Creates new buttons for attacking a specific enemy.
        """
        self.bg_canvas.delete("attack_button1", "attack_button2",
                              "attack_button3", "attack_button4")
        if len(self.enemies) > 0:
            Button(self, "Attack #0", lambda: self.player_attack(self.enemies[0]),
                   50, 680, font=("Cambria Math", 12, "bold"), tags="attack_button1")
        if len(self.enemies) > 1:
            Button(self, "Attack #1", lambda: self.player_attack(self.enemies[1]),
                   200, 680, font=("Cambria Math", 12, "bold"), tags="attack_button2")
        if len(self.enemies) > 2:
            Button(self, "Attack #2", lambda: self.player_attack(self.enemies[2]),
                   350, 680, font=("Cambria Math", 12, "bold"), tags="attack_button3")
        if len(self.enemies) > 3:
            Button(self, "Attack #3", lambda: self.player_attack(self.enemies[0]),
                   500, 680, font=("Cambria Math", 12, "bold"), tags="attack_button4")

    def player_attack(self, enemy: Enemy):
        """Method governing how a Player attacks a specified target.
        Args:
            enemy (Enemy): The enemy instance in the enemies attribute to
             attack. Determined by what attack button is used.
        """
        self.player_txt1 = ""
        if not self.player.living:
            return
        if enemy in self.enemies:
            damage = enemy.take_damage(self.player)
            if damage == 0:
                self.player_txt1 += (f"You attacked {enemy.name} but"
                                     f" they dodged!\n")
            else:
                self.player_txt1 += (f"You hit {enemy.name} for {damage}"
                                     f" damage.\n")
            if enemy.stats["Health"] < 1:
                self.enemies.remove(enemy)
                self.room.enemies_killed += 1
                enemy.set_living(False)
                self.player_txt1 += f"You killed {enemy.name}.\n"
                self.player.stats["XP"] += int(enemy.stats["Level"] * 2.5)
                self.player.stats["Credits"] += enemy.stats["Level"]
            self.resolve_player_turn()
        else:
            pass
        if self.player.living:
            self.update_combat_gui()

    def defend(self, defender: Character):
        """Method to temporarily increase a Character's defense
        Args:
            defender (Character): The Character instance that is defending.
        """
        defender.defend_action()
        if isinstance(defender, Player):
            self.player_txt1 = ""
            self.player_txt1 += (f"You are defending.\nYour defense is"
                                 f" temporarily increased to"
                                 f" {self.player.defense}.")
            self.resolve_player_turn()
        if self.player.living:
            self.update_combat_gui()

    def use_medkit(self):
        """Method to use a medkit and update the display.
        """
        self.player_txt1 = ""
        if self.player.stats["Medkits"] > 0:
            heal = self.player.use_medkits()
            self.player_txt1 = (f"You used a medkit and healed for {heal}"
                                f" health.")
        else:
            self.player_txt1 = f"Oops! You ran out of medkits."
        self.resolve_player_turn()
        self.update_combat_gui()

    def resolve_player_turn(self):
        """Method to resolve enemy actions after the player's turn is over.
        """
        if self.player:
            self.player_txt2 = self.player_txt1
            self.player_txt1 = ""
            self.enemy_txt1 = ""
            self.enemy_txt2 = ""
            for enemy in self.enemies:
                enemy.update_defense()
                if self.player.living:
                    self.enemy_turn(enemy)
                self.set_enemy_actions(enemy)
            self.player.update_defense()
            self.combat_log()
            self.turn_count()

    def enemy_turn(self, enemy: Enemy):
        """Method to randomly determine what an Enemy instance does.
        Args:
            enemy (Enemy): The Enemy instance doing the action.
        """
        if enemy.action == "attack":
            damage = self.player.take_damage(enemy)
            if damage == 0:
                self.enemy_txt1 += (f"{self.enemies.index(enemy)})"
                                    f" {enemy.name} attacked"
                                    f" {self.player.name} but you dodged!\n")
            else:
                self.enemy_txt1 += (f"{self.enemies.index(enemy)})"
                                    f" {enemy.name} attacked {self.player.name}"
                                    f" for {damage} damage.\n")
            if self.player.stats["Health"] < 1:
                self.player.set_living(False)
                self.enemy_txt1 += "You were killed!\n"
                self.character_dead_gui()
        elif enemy.action == "defend":
            self.defend(enemy)
            self.enemy_txt1 += (f"{self.enemies.index(enemy)}) {enemy.name} is"
                                f" defending. Their defense is temporarily"
                                f" {enemy.defense} now.\n")
        else:
            self.enemy_txt1 += (f"{self.enemies.index(enemy)}) {enemy.name}"
                                f" did nothing.\n")

    def set_enemy_actions(self, enemy: Enemy):
        """Randomly sets the enemy's actions.
        Args:
            enemy (Enemy): The enemy instance to set their action.
        """
        enemy.randomize_action()
        enemy_predict_resist = (random.randint(1, 100) +
                                enemy.stats["Intelligence"] +
                                enemy.stats["Level"])
        player_predict_chance = (random.randint(1, 100) +
                                 self.player.stats["Intelligence"]
                                 + self.player.stats["Level"])
        if enemy_predict_resist < player_predict_chance:
            if enemy.action == "nothing":
                self.enemy_txt2 += (f"{self.enemies.index(enemy)})"
                                    f" {enemy.name} chose to do {enemy.action}."
                                    f"\n")
            else:
                self.enemy_txt2 += (f"{self.enemies.index(enemy)})"
                                    f" {enemy.name} chose to {enemy.action}."
                                    f"\n")
        else:
            self.enemy_txt2 += (f"{self.enemies.index(enemy)}) {enemy.name}"
                                f" can't be predicted.\n")

    def turn_count(self):
        """Increments turn_counter by 1.
        Returns:
            turn_counter (int): The current turn.
        """
        self.turn_counter += 1
        return self.turn_counter

    def combat_log(self):
        """Updates the combat log.
        """
        self.bg_canvas.delete("player_txt1", "player_txt2", "enemy_txt1",
                              "enemy_txt2")
        self.bg_canvas.create_text(50, 200, width=200,
                                   font=('Cambria_Math', 13, 'bold'),
                                   fill=self.text_color,
                                   justify="left", anchor="w",
                                   text=f"Last Turn (Turn {self.turn_counter})"
                                   f":\n{self.player_txt2}",
                                   tags="player_txt2")
        self.bg_canvas.create_text(50, 300, width=200,
                                   font=('Cambria_Math', 13, 'bold'),
                                   fill=self.text_color,
                                   justify="left", anchor="w",
                                   text=f"This Turn (Turn "
                                   f"{self.turn_counter + 1})"
                                   f":\nWhat will you do?", tags="player_txt1")
        self.bg_canvas.create_text(self.width / 3, 200, width=300,
                                   font=('Cambria_Math', 13, 'bold'),
                                   fill=self.text_color,
                                   justify="left", anchor="w",
                                   text=f"Last Turn (Turn {self.turn_counter})"
                                   f":\n{self.enemy_txt1}", tags="enemy_txt1")
        self.bg_canvas.create_text(self.width / 3, 350, width=300,
                                   font=('Cambria_Math', 13, 'bold'),
                                   fill=self.text_color,
                                   justify="left", anchor="w",
                                   text=f"This Turn (Turn "
                                   f"{self.turn_counter + 1}):\nYour"
                                   f" Intelligence Stat lets you predict that:"
                                   f"\n{self.enemy_txt2}",
                                   tags="enemy_txt2")

    def make_exit(self):
        """Method to make an exit after the fight is won.
        """
        if not self.enemies:
            Button(self, "Exit", self.end_fight, int(self.width / 2 - 60), 580,
                   font=("Cambria Math", 12, "bold"))
            self.bg_canvas.delete("attack_button", "defend_button",
                                  "use_item_button", "enemy_entry",
                                  "enemy_entry_text")

    def character_dead_gui(self):
        """Display GUI if character dies during combat.
        """
        print("Character is dead")
        self.player.is_in_combat = False
        super().destroy()
        self.game_handler.end_game(False)

    def end_fight(self):
        """Method handling when the instance can be exited and what happens.
        """
        if not self.enemies or not self.player.living:
            self.game_handler.exit_room(self.room)
            self.room.clear_room(True)
            self.destroy()

    def destroy(self):
        """Overrides the standard destroy method. Prevents the fight window
         from being destroyed until the fight ends.
        """
        if not self.enemies or not self.player.living:
            self.player.is_in_combat = False
            super().destroy()
