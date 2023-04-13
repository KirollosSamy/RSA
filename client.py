import socket
from chatter import Chatter

class ClientChatter(Chatter):
    """
    This class extends the Chatter class to provide additional functionality for connecting as a client.
    """
    def connect(self):
        """
        Connects to the server as a client using sockets.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"Connected to server on {self.host}:{self.port}")
        
def main():
    PORT = 1234
    client = ClientChatter('localhost', PORT)
    client.connect()
    client.chat()
    
if __name__ == '__main__':
    main()