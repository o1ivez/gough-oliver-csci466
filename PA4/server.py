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
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)
connection, addr = serverSocket.accept()

while(True):
    #get message
    encodedMessage = connection.recv(1024)
    print("Encrypted Message: " + str(encodedMessage) + "\n")
    decodedMessage = (unpad(block_cipher.decrypt(encodedMessage),32)).decode()
    print("Decrypted Message: " + decodedMessage + "\n")
    
    #hash code
    MACRecv = connection.recv(1024).decode()
    print("MAC recieved: " + MACRecv)
    mPlusS = decodedMessage + sharedSecret
    mPlusSBytes = mPlusS.encode()
    digest = hashlib.sha256(mPlusSBytes)
    calcHash = str(digest.hexdigest())
    print("\nComputing H(m+s) on our end.... \n")
    print("Value of (m+s): " + calcHash + "\n")
    if(calcHash == MACRecv):
        print("Hashes match!! Accept")
    else:
        print("Hashes do not match!! Reject")
    print("--------------------------------------------")
