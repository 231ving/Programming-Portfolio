"""Module for the TextPrinter class.
"""


class TextPrinter:
    """Allows for the printing of text to a tkinter widget.
    """
    def __init__(self, tkinter):
        """Creates the instance.
        """
        self.tkinter = tkinter
        self.ready = True

    # Method of printing defines where text will be printed
    # in regards to other text.
    # In most cases, it will be tk.END.
    def animate_text(self, text, text_id, method_of_printing):
        """Method to print text one character at a time.
        Args:
            text (str): The text string to be printed.
            text_id (str): The text_box to print to.
            method_of_printing: How to print the string.
        Returns:
            None: If the previous text isn't printed yet, nothing happens.
        """
        if self.ready is False:
            return

        self.ready = False

        delta = 25
        delay = 0

        # Offset textbox as text height is constantly changing
        self.offset_text_box(text_id, -21)

        print(f"\ntext {text} is being printed\n")

        for char in text:
            # pylint: disable=C3001
            update_text = lambda s=char: self.tkinter.bg_canvas.insert(text_id, method_of_printing, s)
            self.tkinter.bg_canvas.after(delay, update_text)
            delay += delta

        delay += delta
        self.tkinter.bg_canvas.after(delay, self.toggle_ready)

    def toggle_ready(self):
        """Setter for the ready attribute.
        """
        self.ready = not self.ready

    # def is_text_ready(self):
    #     """Getter for the ready attribute.
    #     Returns:
    #         ready (bool): If the text is done printing yet.
    #     """
    #     return self.ready

    def offset_text_box(self, text_box_id, amount):
        """Method to determine how much to offset the text by.
        Args:
            text_box_id: The text_box id.
            amount: The amount of offsetting.
        """
        self.tkinter.bg_canvas.move(text_box_id, 0, amount)
