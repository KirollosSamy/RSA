class Transmorpher:
    """
    A class for encoding and decoding messages using a custom scheme.
    """
    
    SPACE = 36
    GROUP_SIZE = 5
    BASE = 37

    @classmethod
    def encode(cls, message:str) -> list:
        """
        Encodes a string message into a list of integers.
        
        Args:
        - message (str): The message to encode
        
        Returns:
        - A list of integers representing the encoded message
        """
        numeric = Transmorpher._alpha_map(message)
        n = len(numeric)
        
        #pad the last group with spaces
        rem = n % Transmorpher.GROUP_SIZE
        pad_size = Transmorpher.GROUP_SIZE - rem if rem else 0
        numeric.extend([Transmorpher.SPACE] * pad_size)
        n = n + pad_size
        
        encoded = []        
        for i in range(0, n-Transmorpher.GROUP_SIZE+1, Transmorpher.GROUP_SIZE):
            group = numeric[i:i+Transmorpher.GROUP_SIZE]
            encoded.append(Transmorpher._reduce(group))
        return encoded
        
    @classmethod
    def decode(cls, encoded:list) -> str:
        """
        Decodes a list of integers representing an encoded message into the original string message.
        
        Args:
        - encoded (list): A list of integers representing an encoded message
        
        Returns:
        - The original string message
        """
        message = ''
        for num in encoded:
            group = Transmorpher._inverse_reduce(num)
            message += Transmorpher._inverse_alpha_map(group)
        return message.rstrip()

    @classmethod
    def _alpha_map(cls, message:str) -> list:
        """
        Maps each character in a string to a corresponding integer.
        
        Args:
        - message (str): The string to map
        
        Returns:
        - A list of integers representing the mapped string
        """
        numeric = list(message)
        
        for i, char in enumerate(message):
            if char.isalpha():
                numeric[i] = ord(char) - ord('a') + 10
            elif char.isdigit():
                numeric[i] = int(char)
            else:
                numeric[i] = Transmorpher.SPACE
            
        return numeric

    @classmethod
    def _inverse_alpha_map(cls, numeric:list) -> str:
        """
        Inverse of _alpha_map: maps each integer in a list to a corresponding character in a string.
        
        Args:
        - numeric (list): A list of integers representing the mapped string
        
        Returns:
        - The original string
        """
        str_list = []
        
        for num in numeric:
            if num < 10:
                str_list.append(str(num))
            elif num==Transmorpher.SPACE:
                str_list.append(' ')
            else:
                str_list.append(chr(num + ord('a') - 10))
            
        return "".join(str_list)

    @classmethod
    def _reduce(cls, group:list) -> int:
        """
        Reduces a group of integers into a single integer.
        
        Args:
        - group (list): A list of integers representing a group
        
        Returns:
        - An integer representing the reduced group
        """
        number = 0
        for dig in group:
            number = number * Transmorpher.BASE + dig
        return number

    @classmethod
    def _inverse_reduce(cls, number:int) -> list:
        """
        Converts a given decimal number to a list of digits in a specified base. 
        The base to use is determined by the Transmorpher.BASE constant.

        Args:
        - number (int): An integer representing the reduced group
        
        Returns:
        - An integer representing the reduced group
        """
        group = list([None]*Transmorpher.GROUP_SIZE)
        
        for i in range(Transmorpher.GROUP_SIZE):
            term = number % Transmorpher.BASE
            group[Transmorpher.GROUP_SIZE-i-1] = term
            number = (number-term) // 37
        return group
