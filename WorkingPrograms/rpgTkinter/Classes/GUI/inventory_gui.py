"""Module for the InventoryGUI class.
"""


import tkinter as tk
from PIL import ImageTk, Image
from Classes.GUI.button import Button
from Classes.character import Player
from Classes.Rooms.room import Room


class InventoryGUI(tk.Toplevel):
    """Class governing actions involving a Player instance's equipment
     and inventory.
    """
    def __init__(self, player: Player, room: Room, gui):
        """Creates the instance.
        Args:
            player (Player): The Player instance to interact with.
            room (Room): The room the Player instance is in.
            gui: The MainGui instance that is a parent of this instance.
        """

        super().__init__()
        self.title("Character Inventory")
        self.geometry(f'{1000}x{600}+150+50')
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.minsize(self.width, self.height)  # Min size, can be maximized.
        self.iconbitmap('Images/LevelOne/SpaceShip.ico')
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.player = player
        self.room = room
        self.gui = gui
        self.item_entry = None
        self.inventory_text = ""

        self.original_image = Image.open('Images/LevelOne/Inventory2.jpg').resize((self.width, self.height))
        self.bg = ImageTk.PhotoImage(self.original_image)

        self.bg_canvas = tk.Canvas(self, width=self.width, height=self.height,
                                   bg="#043F5B")
        self.bg_canvas.pack(fill='both', expand=True)
        self.bg_canvas.create_image(0, 0, image=self.bg, anchor='nw')

        Button(self, "Close", self.destroy, self.width - 150, 580, font=("Times New Roman", 15))

        self.bg_canvas.create_text(self.width / 2 - 200, self.height - 580,
                                   font="Cambria_Math 12 bold", fill="#FFFFFF",
                                   justify="center",
                                   text=self.player.name + "'s Equipment",
                                   tags="equipment_title")
        self.bg_canvas.create_text(self.width / 2 + 200, self.height - 580,
                                   font="Cambria_Math 12 bold", fill="#FFFFFF",
                                   justify="center",
                                   text=self.player.name + "'s Inventory",
                                   tags="inventory_title")

        Button(self, "Unequip Entered Item\nFrom Equipment",
               self.remove_equipped_item, 150, 400,
               font=("Times New Roman", 15))
        Button(self, "Equip Entered Item\nFrom Inventory",
               self.equip_item_inventory, 350, 400,
               font=("Times New Roman", 15))
        Button(self, "Drop Entered Item\nFrom Inventory",
               self.drop_item_inventory, 550, 400,
               font=("Times New Roman", 15))

        self.item_entry_text = tk.Label(self, text='Enter Item Below To Start',
                                        font='Time_New_Roman 10')
        self.item_entry_text_window = self.bg_canvas.create_window(150, 450,
                                                                   anchor='sw',
                                                                   window=self.item_entry_text, tags="item_entry_text")
        self.item_entry_box = tk.Entry(self, font='Time_New_Roman 12')
        self.bg_canvas.create_window(150, 480, anchor='sw',
                                     window=self.item_entry_box,
                                     tags="item_entry")

        self.update_inventory_gui()
        self.mainloop()

    def equipment_grid(self):
        """Create and update the display containing information about the
         Player's equipment.
        """
        self.bg_canvas.delete("equipment")
        if self.player.equipment:
            self.bg_canvas.create_text(self.width / 2 - 200, self.height - 450,
                                       font=8,
                                       fill="#FFFFFF", text="\nHead Armor....."
                                       + str(self.player.equipment["Head"].stats["name"])
                                       + " +" + str(self.player.equipment["Head"].stats["defense"])
                                       + " Defense" + "\nArm Armor......"
                                       + str(self.player.equipment["Arms"].stats["name"])
                                       + " +" + str(self.player.equipment["Arms"].stats["defense"])
                                       + " Defense" + "\nChest Armor...."
                                       + str(self.player.equipment["Chest"].stats["name"]) + " +"
                                       + str(self.player.equipment["Chest"].stats["defense"])
                                       + " Defense" + "\nLeg Armor......."
                                       + str(self.player.equipment["Legs"].stats["name"])
                                       + " +" + str(self.player.equipment["Legs"].stats["defense"])
                                       + " Defense" + "\nFoot Armor......"
                                       + str(self.player.equipment["Feet"].stats["name"])
                                       + " +" + str(self.player.equipment["Feet"].stats["defense"])
                                       + " Defense" + "\nWeapon..........."
                                       + str(self.player.equipment["Weapon"].stats["name"]) + " +"
                                       + str(self.player.equipment["Weapon"].stats["damage"])
                                       + " Damage" + "\n\nTotal Attack....."
                                       + str(self.player.get_attack())
                                       + "\nTotal Defense.."
                                       + str(self.player.get_defense())
                                       + "\nCredits............"
                                       + str(self.player.stats["Credits"]),
                                       tags="equipment", justify="left")

    def inventory_grid(self):
        """Create and update the display containing information about the
         Player's inventory.
        """
        self.bg_canvas.delete("inventory")
        self.inventory_text = ""
        if len(self.player.inventory) > 0:
            for item in self.player.inventory:
                if item.stats["type"] == "Weapon":
                    self.inventory_text += ("\n" + str(item.stats["name"])
                                            + ": +" + str(item.stats["damage"])
                                            + " Damage")
                else:
                    self.inventory_text += ("\n" + str(item.stats["name"]) +
                                            ": +" + str(item.stats["defense"])
                                            + " Defense")
        else:
            self.inventory_text = "Your Inventory\nIs Empty"
        self.bg_canvas.create_text(self.width / 2 + 200, self.height - 450,
                                   font="Cambria_Math 12 bold", fill="#FFFFFF",
                                   justify="center", text=self.inventory_text,
                                   tags="inventory")

    def update_inventory_gui(self):
        """Method to update the entire display.
        """
        self.equipment_grid()
        self.inventory_grid()

    def drop_item_inventory(self):
        """Method to remove an item from the Player instance's inventory.
         Reads input from the entry_box.
        """
        self.read_entry_box()
        if self.read_entry_box() is not None:
            item_to_drop = self.item_entry
            for item in self.player.inventory:
                if item.stats["name"] == item_to_drop:
                    self.player.drop_item(item)
                    self.item_entry_box.delete(0, 100)
                    self.update_inventory_gui()

    def equip_item_inventory(self):
        """Method to equip an item from the Player's inventory.
         Reads input from the entry_box.
        """
        self.read_entry_box()
        if self.read_entry_box() is not None:
            item_to_equip = self.item_entry
            for item in self.player.inventory:
                if item.stats["name"] == item_to_equip:
                    self.player.equip_item(item)
                    self.player.update_defense()
                    self.player.update_attack()
                    self.update_inventory_gui()

    def remove_equipped_item(self):
        """Method to remove an item from the Player's equipment and add it
         to their inventory.
         Reads input from the entry_box.
        """
        self.read_entry_box()
        if self.read_entry_box() is not None:
            item_to_remove = self.item_entry
            for item in self.player.equipment.values():
                if item.stats["name"] == item_to_remove:
                    self.player.unequip_item(item)
                    self.player.update_defense()
                    self.player.update_attack()
                    self.update_inventory_gui()

    def read_entry_box(self) -> None | str:
        """Method to read input from the entry_box.
        Returns:
            item_entry: The string representation of the input in the
             entry_box.
             None if no input was detected.
        """
        self.item_entry = None
        if self.item_entry_box.get():
            self.item_entry = self.item_entry_box.get()
        return self.item_entry

    def destroy(self):
        """Method governing what happens when the widget is closed.
        """
        self.room.clear_room(True)
        self.gui.ready = True
        super().destroy()
