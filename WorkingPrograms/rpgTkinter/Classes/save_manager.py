"""Module governing save files.
"""

from pickle import dump, load


# Manages saving and loading
class SaveManager:
    """Class governing the saving and loading of save data.
    """
    def __init__(self):
        """Creates the Saves folder and the only save file.
        """
        self.file_name = "Saves/save.txt"
        self.file_contents = None

    # Opens save file and return contents as a dictionary
    def get_save(self):
        """Gets the save data.
        Returns:
            file_contents: The save file data
        """
        self.open_save_file()
        return self.file_contents

    # Uses pickle module to open save file
    def open_save_file(self):
        """Opens the save file"""
        with open(self.file_name, "rb") as file:
            self.file_contents = load(file)

    # Uses pickle module to save dictionary to file
    def write_to_save_file(self, save):
        """Writes to file as bytes.
        """
        with open(self.file_name, "wb") as file:
            dump(save, file)

    # Delete save file
    def clear_save_file(self):
        """Clears bytes in file and replaces it with "".
        """
        open(self.file_name, "w").close()

    def is_save_empty(self):
        """Returns boolean value based on state of save.
        """
        with open(self.file_name, "rb") as file:
            t = file.read(1)
            if t:
                return False
            else:
                return True
