"""Module containing the ShopGUI class.
"""
import csv
import random
import tkinter as tk
from PIL import ImageTk, Image
from Classes.GUI.button import Button
from Classes.character import Player
from Classes.Rooms.shop_room import ShopRoom



class ShopGUI(tk.Toplevel):
    """Class governing player actions while the Player instance is in
     a ShopRoom.
    """

    def __init__(self, room: ShopRoom, player: Player, game_handler):
        """Method to equip an item from the Player's inventory.
        Args:
            room (ShopRoom): The ShopRoom instance to interact with
            player (Player): The Player instance to interact with.
            game_handler: The game_handler instance.
        """

        super().__init__()
        self.title("Shop Inventory")
        self.geometry(f'{1100}x{700}+150+50')
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.minsize(self.width, self.height)  # Min size, can be maximized.
        self.iconbitmap('Images/LevelOne/SpaceShip.ico')
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.player = player
        self.shop = room
        self.game_handler = game_handler
        self.item_entry = None
        self.inventory_text = ""
        self.shop_text = ""
        self.armory_names = []

        # Text file where the armory names are saved.
        with open('Names/items_txt/armoryNames.txt',
                  'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                self.armory_names.extend(row)

        self.original_image = Image.open('Images/LevelOne/ShopStore2.jpg').resize((self.width, self.height))
        self.bg = ImageTk.PhotoImage(self.original_image)

        self.bg_canvas = tk.Canvas(self, width=self.width, height=self.height,
                                   bg="black")
        self.bg_canvas.pack(fill='both', expand=True)
        self.bg_canvas.create_image(0, 0, image=self.bg, anchor='nw')
        self.frame = Image.open('Images/Items/ShopFrame.jpg').resize((100, 600))
        self.item_frame = ImageTk.PhotoImage(self.frame)
        self.bg_canvas.create_image(self.width - 120, 20, image=self.item_frame, anchor='nw')

        # Six Randomized item to show on the screen.
        self.armory_names = random.sample(self.armory_names, 6)
        self.image_space = 150
        self.photo_images = []

        for counter, name in enumerate(self.armory_names):
            image = Image.open(f'Images/Items/{name}.png').resize((60, 60))
            photo_image = ImageTk.PhotoImage(image)

            #   Adds  each image to the list and adds it on the Canvas.
            self.photo_images.append(photo_image)
            self.bg_canvas.create_image(self.width - 110, self.image_space, image=photo_image, anchor='nw')

            #   Increment the test variable for the next image position
            self.image_space += 60

        #   Icons identifying stats
        self.attack_icon = Image.open('Images/Items/Attack.png').resize((30, 30))
        self.att_stat_icon = ImageTk.PhotoImage(self.attack_icon)

        self.def_icon = Image.open('Images/Items/defense.png').resize((30, 30))
        self.deff_stat_icon = ImageTk.PhotoImage(self.def_icon)

        self.med_image = Image.open('Images/Items/Medkit.png').resize((30, 30))
        self.med_kit_image = ImageTk.PhotoImage(self.med_image)

        self.credit_icon = Image.open('Images/Items/Coin2.png').resize((30, 30))
        self.credit_stat_icon = ImageTk.PhotoImage(self.credit_icon)

        self.bg_canvas.create_image(50, self.height - 450, image=self.att_stat_icon, anchor='nw')
        self.bg_canvas.create_image(50, self.height - 410, image=self.deff_stat_icon, anchor='nw')
        self.bg_canvas.create_image(50, self.height - 370, image=self.med_kit_image, anchor='nw')
        self.bg_canvas.create_image(50, self.height - 330, image=self.credit_stat_icon, anchor='nw')

        Button(self, "Close", self.destroy, self.width - 160, self.height - 20, font=("Cambria Math", 12, "bold"))

        self.bg_canvas.create_text(self.width / 2 - 350, self.height - 650,
                                   font='Cambria_Math 14 bold', fill="#69FAE4", justify="left",
                                   text=self.player.name + "'s Equipment",
                                   tags="equipment_title")
        self.bg_canvas.create_text(self.width / 2, self.height - 650,
                                   font='Cambria_Math 14 bold', fill="#69FAE4", justify="left",
                                   text=self.player.name + "'s Inventory",
                                   tags="inventory_title")
        self.bg_canvas.create_text(self.width / 2 + 260, self.height - 650,
                                   font='Cambria_Math 14 bold', fill="#69FAE4", justify="left",
                                   text=self.shop.name + "'s Shop",
                                   tags="shop_title")

        Button(self, "Unequip Entered Item\nFrom Equipment",
               self.remove_equipped_item, 20, 620,
               font=("Cambria Math", 12, "bold"))
        Button(self, "Equip Entered Item\nFrom Equipment",
               self.equip_item_inventory, 190, 620,
               font=("Cambria Math", 12, "bold"))
        Button(self, "Purchase Entered Item\nFrom Shop",
               self.buy_item_from_shop, 525, 620,
               font=("Cambria Math", 12, "bold"))
        Button(self, "Sell Entered Item", self.sell_item_inventory, 360, 555,
               font=("Cambria Math", 12, "bold"))
        Button(self, "Buy Medkit\nFor 3 Credits", self.buy_medkits, 700, 620,
               font=("Cambria Math", 12, "bold"))

        self.item_entry_text = tk.Label(self, text='Enter Item Below To Start',
                                        font='Cambria_Math 10 bold')
        self.item_entry_text = self.bg_canvas.create_window(self.width / 2 - 205, 585, anchor='sw',
                                                            window=self.item_entry_text, tags="item_entry_text")
        self.item_entry_box = tk.Entry(self, font='Cambria_Math 12 bold',
                                       highlightthickness=2, highlightbackground="#69FAE4")
        self.bg_canvas.create_window(self.width / 2 - 215, 615, anchor='sw',
                                     window=self.item_entry_box,
                                     tags="item_entry")

        self.update_shop_gui()
        self.mainloop()

    def equipment_grid(self):
        """Creates and updates the Player instance's equipment display.
        """
        self.bg_canvas.delete("equipment")
        if self.player.equipment:
            self.bg_canvas.create_text(self.width / 2 - 300, self.height - 450,
                                       font="Cambria_Math 13 bold",
                                       fill="#69FAE4", justify="left",
                                       text="\nHead Armor:\t"
                                            + str(self.player.equipment["Head"].stats["name"]) + ":\t+"
                                            + str(self.player.equipment["Head"].stats["defense"])
                                            + " Defense" + "\nArm Armor:\t"
                                            + str(self.player.equipment["Arms"].stats["name"]) + ":\t+"
                                            + str(self.player.equipment["Arms"].stats["defense"])
                                            + " Defense" + "\nChest Armor:\t"
                                            + str(self.player.equipment["Chest"].stats["name"]) + ":\t+"
                                            + str(self.player.equipment["Chest"].stats["defense"])
                                            + " Defense" + "\nLeg Armor:\t"
                                            + str(self.player.equipment["Legs"].stats["name"]) + ":\t+"
                                            + str(self.player.equipment["Legs"].stats["defense"])
                                            + " Defense" + "\nFoot Armor:\t"
                                            + str(self.player.equipment["Feet"].stats["name"]) + ":\t+"
                                            + str(self.player.equipment["Feet"].stats["defense"])
                                            + " Defense" + "\nWeapon:\t\t"
                                            + str(self.player.equipment["Weapon"].stats["name"]) + ":\t+"
                                            + str(self.player.equipment["Weapon"].stats["damage"])
                                            + " Damage" + "\n\n\tTotal Attack:\t"
                                            + str(self.player.get_attack()) +
                                            "\n\n\tTotal Defense:\t"
                                            + str(self.player.get_defense())
                                            + "\n\n\tMedkits:\t"
                                            + str(self.player.med_kits)
                                            + "\n\n\tCredits:\t"
                                            + str(self.player.stats["Credits"]),
                                       tags="equipment")

    def inventory_grid(self):
        """Creates and updates the Player instance's inventory display.
        """
        self.bg_canvas.delete("inventory")
        self.inventory_text = ""
        if len(self.player.inventory) > 0:
            for item in self.player.inventory:
                if item.stats["type"] == "Weapon":
                    self.inventory_text += ("\n" + str(item.stats["name"]) +
                                            ": +" + str(item.stats["damage"])
                                            + " Damage" + "\nValue: "
                                            + str(item.stats["value"]))
                else:
                    self.inventory_text += ("\n" + str(item.stats["name"]) +
                                            ": +" + str(item.stats["defense"])
                                            + " Defense" + "\nValue: " +
                                            str(item.stats["value"]))
        else:
            self.inventory_text = "Your Inventory\nIs Empty"
        self.bg_canvas.create_text(self.width / 2 + 20, self.height - 450,
                                   font='Cambria_Math 13 bold', fill="#69FAE4",
                                   justify="left", text=self.inventory_text,
                                   tags="inventory")

    def shop_grid(self):
        """Creates and updates the ShopRoom instance's items.
        """
        self.bg_canvas.delete("shop")
        self.shop_text = ""
        if len(self.shop.items) > 0:
            for item in self.shop.items:
                if item.stats["type"] == "Weapon":
                    self.shop_text += ("\n" + str(item.stats["name"]) + ": +"
                                       + str(item.stats["damage"]) + " Damage"
                                       + "\nValue: "
                                       + str(item.stats["value"]))
                else:
                    self.shop_text += ("\n" + str(item.stats["name"]) + ": +"
                                       + str(item.stats["defense"])
                                       + " Defense" + "\nValue: " +
                                       str(item.stats["value"]))
        else:
            self.shop_text = "The Shop Is Empty"
        self.bg_canvas.create_text(self.width / 2 + 270, self.height - 450,
                                   font='Cambria_Math 14 bold', fill="#69FAE4",
                                   justify="left", text=self.shop_text,
                                   tags="shop")

    def update_shop_gui(self):
        """Calls on and updates the entire display.
        """
        self.equipment_grid()
        self.inventory_grid()
        self.shop_grid()

    def equip_item_inventory(self):
        """Method to read input from an entry_box and equip the specified Item.
        """
        self.read_entry_box()
        if self.read_entry_box() is not None:
            item_to_equip = self.item_entry
            for item in self.player.inventory:
                if item.stats["name"] == item_to_equip:
                    self.player.equip_item(item)
                    self.player.update_defense()
                    self.player.update_attack()
                    self.update_shop_gui()

    def remove_equipped_item(self):
        """Method to read input from an entry_box and unequip the
         specified Item.
        """
        self.read_entry_box()
        if self.read_entry_box() is not None:
            item_to_remove = self.item_entry
            for item in self.player.equipment.values():
                if item.stats["name"] == item_to_remove:
                    self.player.unequip_item(item)
                    self.player.update_defense()
                    self.player.update_attack()
                    self.update_shop_gui()

    def buy_item_from_shop(self):
        """Method to read input from an entry_box and buy the specified
         Item from the ShopRoom.
        """
        self.read_entry_box()
        if self.read_entry_box() is not None:
            item_to_buy = self.item_entry
            for item in self.shop.items:
                if item.stats["name"] == item_to_buy:
                    if self.player.stats["Credits"] >= item.stats["value"]:
                        self.player.add_item(item)
                        self.shop.items.remove(item)
                        self.player.stats["Credits"] -= item.stats["value"]
                        self.update_shop_gui()

    def sell_item_inventory(self):
        """Method to read input from an entry_box and sell the specified
         Item to the ShopRoom.
        """
        self.read_entry_box()
        if self.read_entry_box() is not None:
            item_to_sell = self.item_entry
            for item in self.player.inventory:
                if item.stats["name"] == item_to_sell:
                    self.player.drop_item(item)
                    self.player.stats["Credits"] += item.stats["value"]
                    self.shop.items.append(item)
                    self.update_shop_gui()

    def buy_medkits(self):
        """Method for the Player instance to buy Medkits in exchange
         for Credits.
        """
        if self.player.stats["Credits"] >= 3:
            self.player.med_kits = 1
            self.player.stats["Credits"] -= 3
            self.update_shop_gui()

    def read_entry_box(self) -> None | str:
        """Method to read input from an entry_box.
        Returns:
            item_entry: The string representation of the input.
             None if no input was detected.
        """
        self.item_entry = None
        if self.item_entry_box.get():
            self.item_entry = self.item_entry_box.get()
        return self.item_entry

    def destroy(self):
        """Method governing what happens when the instance is destroyed.
        """
        self.shop.clear_room(True)
        self.game_handler.exit_room(self.shop)
        super().destroy()
