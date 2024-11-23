import random
import hashlib
import socket

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

#encryption set up
key = "0123456789ABCDEF"
sharedSecret = "csci466"
block_cipher = AES.new(key.encode(), AES.MODE_ECB) #create block cypher

#set up socket
port = 9000
host = socket.gethostname()
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host,port))

while(True):
    #get message input and send over info
    print("Enter message to send: ")
    message = input()
    ciphertext = block_cipher.encrypt(pad(message.encode(),32)) #encrypt data
    clientSocket.send(ciphertext)
    #50:50 curruption
    coin = random.randint(0, 100)
    if(coin > 50 ):
        pass
    else:
        message = message + "0"
        print("(Data has been currupted/tampered/spoofed)")
    #compute H(m+s)
    mPlusS = message + sharedSecret
    mPlusSBytes = mPlusS.encode()
    digest = hashlib.sha256(mPlusSBytes)
    print("Value of (m+s): " + str(digest.hexdigest()))
    clientSocket.send(str(digest.hexdigest()).encode())
    print()
