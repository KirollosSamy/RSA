import socket
import threading
import json
from rsa import RSA
from transmorpher import Transmorpher

class Chatter:
    """
    This class provides the functionality for a two-way chat between two parties connected using sockets. 
    It uses RSA encryption to secure the communication between the two parties.
    
    """
    
    def __init__(self, host, port):
        """
        Initializes the Chatter object with a host and port.
        
        Args:
            host (str): The IP address of the host
            port (int): The port number of the connection
        """
        self.host = host
        self.port = port
        self.exit = False
    
    def connect(self):
        """
        Connects to the host and port specified in the attributes using sockets.
        """
        raise NotImplementedError("Must implement this function")
            
    def receive(self, rsa):
        """
        Receives messages and decrypts them using the provided RSA object. If the message received is 'exit', 
        the chat will be terminated. This method runs indefinitely until 'exit' is received or self.exit is True.
        
        Args:
            rsa (RSA): An RSA object used for encryption and decryption.
        """
        while True:
            if self.exit: return
            try:
                message = self.socket.recv(1024)
                plaintext = rsa.decrypt(message)
                if self.exit or plaintext == "exit": 
                    self.exit = True
                    print("Other chatter disconnected, enter anything to exit")
                    return
                print(f"Received message: {plaintext}")
            except socket.error: pass
            

    def send(self, rsa):
        """
        Sends messages and encrypts them using the provided RSA object. If the message sent is 'exit', 
        the chat will be terminated. This method runs indefinitely until 'exit' is sent or self.exit is True.
        
        Args:
            rsa (RSA): An RSA object used for encryption and decryption.
        """
        while True:
            message = input()
            ciphertext = rsa.encrypt(message)
            self.socket.send(ciphertext)
            if self.exit or message == "exit": 
                self.exit = True
                return
            
            
    def chat(self):
        """
        Initiates the chat by generating RSA keys and exchanging them with the other party. The chat terminates when 
        'exit' is sent or received. This method creates two threads, one for sending messages and the other for receiving 
        messages.
        """

        rsa = RSA(Transmorpher, 64)
        print("Generating keys")
        my_PU = rsa.generate_keys()
        print("Exchanging keys")
        self.socket.send(json.dumps(my_PU).encode('utf-8'))
        rsa.encryption_key = tuple(json.loads(self.socket.recv(1024).decode('utf-8')))
        
        self.socket.setblocking(False)
        
        print("Chat started")
        thread_receive = threading.Thread(target=self.receive, args=(rsa,))
        thread_receive.start()

        thread_send = threading.Thread(target=self.send, args=( rsa,))
        thread_send.start()
        
        thread_receive.join()
        thread_send.join()
        
        print("chat terminated")
        