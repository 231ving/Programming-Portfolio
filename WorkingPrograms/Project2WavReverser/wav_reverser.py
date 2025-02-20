"""This file obtains the header information from an audio file, stores the audio
 file's contents in the form of frames, and allows for the creation of a reversed
  audio file.

Requires the original audio file to be in the same folder as this python file.

Phuc Le
10/8/2023
Version 4.0
"""


class WaveHeader:
    """The WaveHeader class takes the first 44 bytes of an audio file and stores
    information from it into various attributes.
    Attributes:
        __file_size (int): The file size in bytes minus 8.
        __num_channel (int): The number of channels.
        __sample_rate (int): The number of samples taken each second.
        __bytes_per_sample (int): The number of bytes per sample.
        __data_sec_size (int): The data section size.
        __header (object): The complete audio file header.
    """
    def __init__(self, header_bytes: bytes):
        """The constructor for the WaveHeader class. It separates the bytes
         given into the various attributes.
        Args:
            header_bytes (???): The first 44 bytes of an audio file.
        """
        self.__file_size = int.from_bytes(header_bytes[4:8], 'little')
        self.__num_channel = int.from_bytes(header_bytes[22:24], 'little')
        self.__sample_rate = int.from_bytes(header_bytes[24:28], 'little')
        self.__bytes_per_sample = int.from_bytes(header_bytes[34:36], 'little') // 8
        self.__data_sec_size = int.from_bytes(header_bytes[40:44], 'little')
        self.__header = header_bytes[0:44]

    def get_file_size(self) -> int:
        """Getter for the __file_size attribute.
        Returns:
            __file_size (int): The file size in bytes minus 8.
        """
        return self.__file_size

    def get_num_channel(self) -> int:
        """Getter for the __num_channel attribute.
        Returns:
            __num_channel (int): The number of channels.
        """
        return self.__num_channel

    def get_sample_rate(self) -> int:
        """Getter for the __sample_rate attribute.
        Returns:
            __sample_rate (int): The number of samples taken each second.
        """
        return self.__sample_rate

    def get_bytes_per_sample(self) -> int:
        """Getter for the __bytes_per_sample attribute.
        Returns:
            __bytes_per_sample (int): The number of bytes per sample.
        """
        return self.__bytes_per_sample

    def get_data_sec_size(self) -> int:
        """Getter for the __data_sec_size attribute.
        Returns:
            __data_sec_size (int): The data section size.
        """
        return self.__data_sec_size

    def get_header(self) -> object:
        """Getter for the __header attribute.
        Returns:
            __header (object): The complete audio file header.
        """
        return self.__header

    def set_file_size(self, file_size: int):
        """Setter for the __file_size attribute.
        Args:
            file_size (int): The new file size in bytes minus 8.
        """
        self.__file_size = file_size

    def set_num_channel(self, num_channel: int):
        """Setter for the __num_channel attribute.
        Args:
            num_channel (int): The new number of channels.
        """
        self.__num_channel = num_channel

    def set_sample_rate(self, sample_rate: int):
        """Setter for the __sample_rate attribute.
        Args:
            sample_rate (int): The new number of samples taken each second.
        """
        self.__sample_rate = sample_rate

    def set_bytes_per_sample(self, bytes_per_sample: int):
        """Setter for the __bytes_per_sample attribute.
        Args:
            bytes_per_sample (int): The new number of bytes per sample.
        """
        self.__bytes_per_sample = bytes_per_sample

    def set_data_sec_size(self, data_sec_size: int):
        """Setter for the __data_sec_size attribute.
        Args:
            data_sec_size (int): The new data section size.
        """
        self.__data_sec_size = data_sec_size


class Frame:
    """The Frame class takes in a list of bytes and turns it into a frame using
     information taken from the WaveFile instance.
    Attributes:
        __bytes_in_sample (int): The number of bytes in one sample.
        __num_channel (int): The number of channels.
        __bytes_list (bytes): The bytes given.
        __frame (list[bytes]): The list of bytes in one frame.
    """
    def __init__(self, bytes_in_sample: int, num_channel: int, bytes_list: bytes):
        """The constructor for the Frame class.
        Args:
            bytes_in_sample (int): The number of bytes in each sample.
            num_channel (int): The number of channels used.
            bytes_list (bytes): The bytes meant to go in the frame.
        """
        self.__bytes_in_sample = bytes_in_sample
        self.__num_channel = num_channel
        self.__bytes_list = bytes_list
        self.__frame = []

    def get_bytes_in_sample(self) -> int:
        """Getter for the __bytes_in_sample attribute.
        Returns:
            __bytes_in_sample (int): The number of bytes in one sample.
        """
        return self.__bytes_in_sample

    def get_num_channel(self) -> int:
        """Getter for the __num_channel attribute.
            Returns:
            __num_channel (int): The number of channels.
        """
        return self.__num_channel

    def get_bytes_list(self) -> bytes:
        """Getter for the __bytes_list attribute.
        Returns:
            __bytes_list (bytes): The bytes given.
        """
        return self.__bytes_list

    def get_frame(self) -> list[bytes]:
        """Getter for the __frame attribute.
        Returns:
            __frame (list[bytes]): The list of bytes in one frame.
        Raises:
            ValueError: If the number of bytes given doesn't match the expected
             number of bytes in a frame.
        """
        if len(self.__bytes_list) == self.__bytes_in_sample * self.__num_channel:
            for byt in self.__bytes_list:
                self.__frame.append(int.to_bytes(byt, 1, 'little'))
        else:
            raise ValueError("Number of bytes given doesn't match the "
                             "number of bytes meant to go in one frame.")
        return self.__frame


class WaveFile:
    """The WaveFile class takes a file path to an audio file, sends the first
     44 bytes to the WaveHeader class, and then organizes the rest of the bytes
      into frames.
    Attributes:
        __wave_header (bytes): The full wave header in bytes.
        __frame_list (list[list[bytes]]): The list containing the Frame objects
         in the audio file.
    """
    def __init__(self, file_path: str):
        """The constructor for the WaveFile class.
        Args:
            file_path (str): The file path for the audio file we want to look at.
        """
        with open(file_path, "rb") as audio:
            self.__bts = audio.read()

        self.__z = WaveHeader(self.__bts[0:44])
        self.__wave_header = self.__z.get_header()
        self.__frame_list = []
        self.__frame_size = (self.__z.get_bytes_per_sample() *
                             self.__z.get_num_channel())

        for i in range(44, len(self.__bts), self.__frame_size):
            self.__frame_bytes = self.__bts[i: i + self.__frame_size]
            frame = Frame(self.__z.get_bytes_per_sample(),
                          self.__z.get_num_channel(), self.__frame_bytes)
            self.__frame_list.append(frame.get_frame())

    def get_wave_header(self) -> bytes:
        """Getter for the __wave_header attribute.
        Returns:
            __wave_header (bytes): The full wave header in bytes.
        """
        return self.__wave_header  # Not sure why PyCharm says this is an object

    def get_frame_list(self) -> list[list[bytes]]:
        """Getter for the __frame_list attribute.
         Returns:
             __frame_list (list[list[bytes]]): The list containing the frames
              in the audio file.
        """
        return self.__frame_list

    def reverse_file(self, file_name: str):
        """Writes a new reversed audio file.
        Args:
            file_name (str): The file to write the reversed audio into.
        """
        with open(file_name, 'wb') as reverse_file:
            self.__frame_list.reverse()
            reverse_file.write(self.__z.get_header())
            for frame in self.__frame_list:
                for byte in frame:
                    reverse_file.write(byte)
