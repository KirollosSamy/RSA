# RSA implementation in Python

[![Python Version](https://img.shields.io/badge/python-3.10.9-blue.svg)](https://www.python.org/downloads/release/python-385/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [RSA implementation in Python](#rsa-implementation-in-python)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Code Walkthrough](#code-walkthrough)
    - [transmorpher.py](#transmorpherpy)
    - [rsa.py](#rsapy)
    - [chatter.py](#chatterpy)
    - [client.py \& server.py](#clientpy--serverpy)
    - [break\_rsa.ipynb](#break_rsaipynb)

## Installation

To install the dependencies, run the following commands:

```bash
pip install pycryptodome
pip install socket
pip install tqdm
pip install matplotlib
```


## Usage

To use the program, split the terminal and run the server and client chatters in separate terminals

To run the Server use the command:

```bash
python server.py
```

To run the Client use the command:

```bash
python client.py
```
Please make sure to run the server first and then the client

To close the chat simply type
```bash
exit
```

That's it! you can start chatting now and all your conversations are secured with RSA 🔒

## Code Walkthrough

### transmorpher.py
The `Transmorpher` class is responsible for encoding and decoding messages.

### rsa.py
This is the core class where RSA encryption and decryption is implemented. The class constructor takes the key size in bits and a class for encoding/decoding (`Transmorpher`). Dependency injection is used so that the RSA class doesn't depend on how the encoding/decoding is done, and different schemes can be used without any changes to the RSA class. The class includes the following public methods:

- `generate_keys()`
- `encrypt()`
- `decrypt()`

### chatter.py
The `Chatter` class is a virtual class responsible for handling the sockets and threading. It has two main methods:

- `connect()`
- `chat()`

The two classes `ClientChatter` and `ServerChatter` inherit from this class and implement the virtual function `connect()`.

### client.py & server.py
The `ClientChatter` and `ServerChatter` classes are defined here. In the main function, an object of each chatter is created and used for chatting.


### break_rsa.ipynb
The code for breaking RSA is implemented in this notebook, In addition, the analysis results and conclusions are shown at the end.