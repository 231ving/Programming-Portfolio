"""Module for creating a custom button.
"""

import customtkinter


class Button:
    """Custom buttons."""
    def __init__(self, container, msg: str, command: callable, x: int, y: int,
                 anchor: str = "sw",
                 font: tuple[str, int] = ("Time New Romans", 20), width=140,
                 height=28, padding=10, color="white", hcolor="#CCCCCC",
                 tags=""):
        """Initialize a custom button. Uses the same format as a regular button.
        Args:
            container: The Tkinter window to place the button in
            msg (str): The msg displayed on the button
            command (callable): The command to do when the button is clicked
            x (int): The x-position
            y (int): The y-position
            anchor (str): Where to anchor the button to
            font (tuple[str, int]): The font and font size of the text
            width (int): The width of the button
            height (int): The height of the button
            padding (int): The amount of pixel padding to add
            color (str): The color of the msg text itself
            hcolor (str): The highlight color to use
            tags (str): The tag associated with this button
        """
        button = customtkinter.CTkButton(
            container, font=font, text=msg, command=command, corner_radius=0, text_color="black", hover_color=hcolor,
            border_spacing=padding, fg_color=color, width=width, height=height, bg_color=color)
        container.bg_canvas.create_window(x, y, anchor=anchor, window=button, tags=tags)
