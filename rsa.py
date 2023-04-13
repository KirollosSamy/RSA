from Crypto.Util.number import GCD, getPrime, inverse
from Crypto.Random.random import randint
from math import floor, ceil, log, sqrt
from tqdm import tqdm

class RSA:
    """
    A class for RSA encryption and decryption.

    """

    def __init__(self, Transmorpher, key_size=1024):
        """
        Initializes the RSA object.

        Args:
        - Transmorpher (object): The Transmorpher object to use for encoding and decoding.
        - key_size (int): The size of the RSA key in bits (default: 1024).
        """
        self.key_size = key_size
        self.Transmorpher = Transmorpher

        # self.num_bytes = ceil((Transmorpher.GROUP_SIZE * log(Transmorpher.BASE, 2)) / 8)
        
        # I believe that this is a reversed dependency the group_size (the number of terms in the representaion of the msg chunk
        # in Transmorpher.BASE) should not be a constant of 5. Instead, RSA class should determine the group size 
        # according to the key_size to ensure that msg chunk < n then num_bytes is simply key_size / 8
        # num_bytes is the number of bytes required to represent a single msg chunk

        # Here's a more practical, generic implementation.
        # Calculate the number of bytes needed for a chunk of plaintext or ciphertext
        Transmorpher.GROUP_SIZE = floor((key_size-1) * log(2, Transmorpher.BASE))
        self.num_bytes = key_size // 8
        
    def generate_keys(self) -> tuple:
        """
        Generates the public and private keys.

        Returns:
        - tuple: The public key (n, e).
        """
        p = getPrime(self.key_size//2)
        q = getPrime(self.key_size//2)

        n = p*q
        phi = (p-1)*(q-1)

        e = randint(1, phi)
        while(GCD(e, phi) != 1):
            e = randint(1, phi)

        d = inverse(e, phi)

        self._PU = (n, e)
        self._PR = (n, d)
        
        return self._PU

    def encrypt(self, plaintext: str) -> bytes:
        """
        Encrypts a plaintext message.

        Args:
        - plaintext (str): The plaintext message to encrypt.

        Returns:
        - bytes: The encrypted ciphertext.
        """
        plaintext = self.Transmorpher.encode(plaintext)

        ciphertext = bytes()
        for chunk in plaintext:
            chunk_ciphertext = self._encrypt(chunk)
            ciphertext += chunk_ciphertext.to_bytes(self.num_bytes, 'little')

        return ciphertext

    def decrypt(self, ciphertext: bytes, PR: tuple = None) -> str:
        """
        Decrypts a ciphertext message.

        Args:
        - ciphertext (bytes): The ciphertext message to decrypt.
        - PR (tuple): The private key (n, d) to use for decryption (default: self._PR).

        Returns:
        - str: The decrypted plaintext message.
        """

        if not PR: PR = self._PR
        
        plaintext = []
        n = len(ciphertext)
        for i in range(0, n-self.num_bytes+1, self.num_bytes):
            chunk_cihpertext = int.from_bytes(ciphertext[i: i+self.num_bytes], 'little')
            plaintext.append(self._decrypt(chunk_cihpertext, PR))
            
        plaintext = self.Transmorpher.decode(plaintext)
        
        return plaintext

    def _encrypt(self, plaintext):
        """
        Encrypts a single chunk of plaintext using the RSA encryption key.

        Args:
        plaintext (int): The chunk of plaintext to encrypt.

        Returns:
        int: The encrypted ciphertext.
        """

        n, e = self._encryption_key
        ciphertext = pow(plaintext, e, n)
        
        return ciphertext
    
    def _decrypt(self, ciphertext, PR):
        """
        Decrypts a single chunk of ciphertext using the RSA private key.

        Args:
        ciphertext (int): The chunk of ciphertext to decrypt.
        PR (tuple): The RSA private key, which consists of the modulus and the decryption exponent.

        Returns:
        int: The decrypted plaintext.
        """

        n, d = PR
        plaintext = pow(ciphertext, d, n)
        
        return plaintext
    
    def break_rsa(self, PU):
        """
        Attempts to break RSA encryption by factoring the modulus using a brute force approach.

        Args:
        PU (tuple): The RSA public key, which consists of the modulus and the encryption exponent.

        Returns:
        tuple: The RSA private key, which consists of the modulus and the decryption exponent.
        """

        n, e = PU
        max = ceil(sqrt(n))+1
        
        print("Breaking RSA...")
        for p in tqdm (range(3, max, 2)):
            if(n % p == 0): break
        print("RSA broken. Welcome to the Matrix.")
        
        q = n // p
        phi = (p-1)*(q-1)
        d = inverse(e, phi)
        
        return (n, d)
    
    @property
    def PU():
        """
        The RSA public key, which consists of the modulus and the encryption exponent.

        Returns:
        tuple: The RSA public key.
        """
        return self._PU
    
    @property
    def encryption_key(self):
        """
        The RSA encryption key, which consists of the modulus and the encryption exponent.

        Returns:
        tuple: The RSA encryption key.
        """
        return self._encryption_key
    
    @encryption_key.setter
    def encryption_key(self, PU):
        """
        Sets the RSA encryption key to the given public key.

        Args:
        PU (tuple): The RSA public key, which consists of the modulus and the encryption exponent.
        """
        self._encryption_key = PU
