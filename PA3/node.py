# Oliver Gough CSCI 466 program 3 10/23/2024
#---------------------------------------------------------Functions---------------------------------------------------------
#Whenever a packet is sent it has a 25% chance to add a packet to the hosts buffer, this handles the chance of that and maybe more
def addToHostBuffer():
    i = random.randint(0, 100)
    if i <= 25:
        return int(1)
    else:
        return int(0)

#-------------------------------------------------------Start of main--------------------------------------------------------

import socket
import sys
import random
import time

#cmd input
sendPort = int(sys.argv[1])
recvPort = int(sys.argv[2])
numOfPacketsInQueue = int(sys.argv[3])
isHead = int(sys.argv[4])
nodeNum = str(sys.argv[5])

#set up recive socket
host = socket.gethostname()
recvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recvSocket.bind((host, recvPort))

#set up send socket
sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send = (host, sendPort)

#if head node ie starts with key
if(isHead == 1):
    print("I am starting with the token!")
    input("Waiting to send until ring is set up ... Press enter to start the head")
    #if buffer is empty send and move on w/ chance of adding to buffer
    if(numOfPacketsInQueue == 0):
        print("I have nothing to send... sending token to next person")
        sendSocket.sendto("".encode(), send)
        numOfPacketsInQueue = int(numOfPacketsInQueue) + addToHostBuffer()
    
    #if buffer is not empty reduce num by 1, send, and maybe add 1
    else:
        print("Sending packet out to internet...")
        numOfPacketsInQueue = numOfPacketsInQueue - 1
        print("Current queue size of Node #" + nodeNum + ": " + str(numOfPacketsInQueue))
        sendSocket.sendto("Token".encode(), send)
        numOfPacketsInQueue = int(numOfPacketsInQueue) + addToHostBuffer()

else:
    print("Node is starting")
    print("Waiting to recieve in while loop...")

while(True):
    data = recvSocket.recvfrom(1024)
    time.sleep(2)
    print("Node " + nodeNum + " has the token!")

    #if buffer is empty send and move on w/ chance of adding to buffer
    if(numOfPacketsInQueue == 0):
        print("I have nothing to send... sending token to next person")
        sendSocket.sendto("".encode(), send)
        numOfPacketsInQueue = int(numOfPacketsInQueue) + addToHostBuffer()
    
    #if buffer is not empty reduce num by 1, send, and maybe add 1
    else:
        print("Sending packet out to internet...")
        numOfPacketsInQueue = numOfPacketsInQueue - 1
        print("Current queue size of Node #" + nodeNum + ": " + str(numOfPacketsInQueue))
        sendSocket.sendto("Token".encode(), send)
        numOfPacketsInQueue = int(numOfPacketsInQueue) + addToHostBuffer()

    print("Sending token to next node...\n")
    print("Waiting to receive in while loop")
