import random
import hashlib
import socket

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = "0123456789ABCDEF"
sharedSecret = "csci466"

#set up socket
port = 9000
host = socket.gethostname()
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))

