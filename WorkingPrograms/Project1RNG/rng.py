"""
This file is meant to generate pseudo-random numbers using the Middle Square,
Linear Congruential, and Lagged Fibonacci methods.

The three random number generators are stored in the MiddleSquare,
LinearCongruential, and LaggedFibonacci classes. The Analyzer class is meant to
analyze the results obtained from said random number generators.

Phuc Le
9/15/2023
Version 3.31
"""


class MiddleSquare:
    """Generates random numbers using the Middle Square method.
    Attributes:
        seed (int): The initial seed to start generating random numbers from.
    """
    def __init__(self, seed: int) -> None:
        """Initializes the MiddleSquare class with a given seed value.
        Args:
            seed (int): The initial seed.
        """
        self.seed = seed
        self.seq_num = set()

    def __iter__(self):
        """Returns the instance of the MiddleSquare class.
        Returns:
            self: The current instance.
        """
        return self

    def __next__(self) -> int:
        """Returns the next number generated using the Middle Square method.
        Returns:
            curr_num (int): The generated random number.
        Raises:
            StopIteration: If the sequence has begun to repeat.
        """
        self.seed_squared = str((int(self.seed) ** 2))
        if len(self.seed_squared) % 2 != 0:
            self.seed_squared = '0' + self.seed_squared
        if len(self.seed_squared) % 2 == 0:
            self.curr_num = (f'{self.seed_squared[len(self.seed_squared) // 2 - 1]}'
                             f'{self.seed_squared[len(self.seed_squared) // 2]}')
        self.curr_num = int(self.curr_num)
        if self.curr_num in self.seq_num:
            raise StopIteration('The sequence values have begun to repeat.')
        self.seq_num.add(self.curr_num)
        self.seed = self.curr_num
        return int(self.curr_num)


class LinearCongruential:
    """Generates random numbers using the Linear Congruential method.
    Attributes:
        seed (int): The initial seed value.
        multiplier (int): The number the seed is multiplied by.
        increment (int): A number added to (seed * multiplier).
        modulus (int): The modulus value.
    """
    def __init__(self, seed: int, multiplier: int, increment: int, modulus: int) -> None:
        """Initialized the LinearCongruential class using the arguments below.
        Args:
            seed (int): The instance's seed value.
            multiplier (int): The instance's multiplier value.
            increment (int): The instance's increment value.
            modulus (int): The instance's modulus value.
        """
        self.seed = seed
        self.multiplier = multiplier
        self.increment = increment
        self.modulus = modulus
        self.seq_num = set()

    def __iter__(self):
        """Returns the instance of the Linear Congruential class.
        Returns:
            self: The current instance.
        """
        return self

    def __next__(self) -> int:
        """Returns the next random number in the Linear Congruential sequence.
        Returns:
            curr_num (int): The generated random number.
        Raises:
            StopIteration: If the sequence has begun to repeat.
        """
        self.curr_num = (((self.multiplier * self.seed) + self.increment)
                         % self.modulus)
        if self.curr_num in self.seq_num:
            raise StopIteration('The sequence values have begun to repeat.')
        self.seq_num.add(self.curr_num)
        self.seed = self.curr_num
        return self.curr_num

    def get_seed(self) -> int:
        """Getter for the seed value.
        Returns:
            seed (int): The current seed value.
        """
        return self.seed

    def get_multiplier(self) -> int:
        """Getter for the multiplier value.
        Returns:
            multiplier (int): The current multiplier value.
        """
        return self.multiplier

    def get_increment(self) -> int:
        """Getter for the increment value.
        Returns:
            increment (int): The current increment value.
        """
        return self.increment

    def get_modulus(self) -> int:
        """Getter for the modulus value.
        Returns:
            modulus (int): The current modulus value.
        """
        return self.modulus


class LaggedFibonacci:
    """Generates random numbers using the Lagged Fibonacci method.
    Attributes:
            seed (int): The instance's seed value.
            j (int): Where the first term is location.
            k (int): Where the second term is location.
            modulus (int): The modulus value.
    """
    def __init__(self, seed: int, j: int, k: int, modulus: int) -> None:
        """Initializes the LaggedFibonacci class with the given arguments.
        Args:
            seed (int): The instance's seed value.
            j (int): The instance's first term location.
            k (int): The instance's second term location.
            modulus (int): The modulus value.
        Raises:
            ValueError: If j < 0 or j > k.
            ValueError: If k is greater than the length of the seed.
        """
        self.seed = seed
        self.j = j
        self.k = k
        self.modulus = modulus
        self.init_seed = str(seed)
        self.curr_seed = ''
        self.seq_num = set()
        if j < 0 or j > k:
            raise ValueError('j < 0 or j > k.')
        if k > len(self.init_seed):
            raise ValueError('k is greater than the length of the seed.')

    def __iter__(self):
        """Returns the instance of the LaggedFibonacci class.
        Returns:
             self: The current instance.
        """
        return self

    def __next__(self) -> int:
        """Returns the next random number in the Lagged Fibonacci sequence.
        Returns:
            curr_num (int): The current random number.
        Raises:
            StopIteration: If the sequence has begun to repeat.
        """
        self.seed = str(self.seed)
        self.curr_num = ((int(self.seed[-self.j]) + int(self.seed[-self.k]))
                         % self.modulus)
        self.seq_num.add(self.curr_num)
        self.seed = self.seed[len(str(self.curr_num)):len(str(self.seed))]
        self.seed += f'{str(self.curr_num)}'
        self.curr_seed += f'{str(self.curr_num)}'
        if self.init_seed in self.curr_seed:
            raise StopIteration('The sequence values have begun to repeat.')
        if self.curr_seed[-len(self.init_seed):] in self.curr_seed[:-len(self.init_seed)]:
            raise StopIteration('The sequence values have begun to repeat.')
        return self.curr_num

    def get_seed(self) -> str:
        """Getter for the seed value.
        Returns:
            seed (str): The currently held seed value.
            #Fucking forgot to change int to str for my submission
        """
        return str(self.seed)

    def get_j(self) -> int:
        """Getter for the j value.
        Returns:
            j (int): The currently held j value.
        """
        return self.j

    def get_k(self) -> int:
        """Getter for the k value.
        Returns:
            k (int): The currently held k value.
        """
        return self.k

    def get_modulus(self) -> int:
        """Getter for the modulus value.
        Returns:
            modulus (int): The currently held modulus value.
        """
        return self.modulus


class Analyzer:
    """Obtains the max, min, average, period, and the bit probability from the
    given RNG generator.
    Attributes:
        rng: The RNG generator class to analyze.
    """
    def __init__(self, rng: object) -> None:
        """Initialize the class and analyze the results of the given RNG
        instance.
        Args:
            rng (object): The RNG class object being analyzed.
        """
        self.__rng = rng
        self.__output = list()
        for num in self.__rng:
            self.__output.append(num)
        self.__max_bits = format(max(self.__output), '0b')
        bits = [0 for _ in range(0, len(self.__max_bits))]
        for i in self.__output:
            self.x = format(i, '0b')
            while len(self.x) != len(self.__max_bits):
                self.x = '0' + self.x
            for a in range(len(self.x)):
                if self.x[a] == '1':
                    bits[a] += 1
        print(f'Max: {max(self.__output)}')
        print(f'Min: {min(self.__output)}')
        print(f'Average: {int(sum(self.__output) / len(self.__output))}')
        print(f'Period: {len(self.__output)}')
        print(f'Monobit Distribution: {bits}')
