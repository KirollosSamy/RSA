import socket
from chatter import Chatter

class ServerChatter(Chatter):
    """
    This class extends the Chatter class to provide additional functionality for connecting as a server.
    """ 
    def connect(self):
        """
        Starts the server and waits for a client to connect using sockets.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        print(f"Server started on {self.host}:{self.port}")
        
        self.socket, _ = server_socket.accept()
        print(f"client connected")
        
def main():
    PORT = 1234
    server = ServerChatter('localhost', PORT)
    server.connect()
    server.chat()

if __name__ == '__main__':
    main()
