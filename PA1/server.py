# Oliver Gough CSCI 466 program 1 server battleship 9/11/2024

import socket
import random
import sys

#server setup
port = int(sys.argv[1])
host = socket.gethostname()

#bind socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind( (host, port) )

#battleship setup code
#create empty 6x6 list for our map
battleShipMap = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

#this code creates a random 4 length ship by first randomly deciding if it is horizontal or verticle and then randomly chosing its starting loction within the bounds 
random_num4ship = random.randint(1,2)
#this case creates verticle down 4 ship
if random_num4ship == 1:
    verticleStart4length = random.randint(0,2)
    horizontalStart4length = random.randint(0,5)
    i = 0
    while i < 4:
        battleShipMap[verticleStart4length+i][horizontalStart4length] = 1
        i = i + 1
#this case creates horizontal across 4 ship
if random_num4ship == 2:
    verticleStart4length = random.randint(0,5)
    horizontalStart4length = random.randint(0,2)
    i = 0
    while i < 4:
        battleShipMap[verticleStart4length][horizontalStart4length+i] = 1
        i = i + 1

#random 3 ship generator
random_num3ship = random.randint(1,2)
#creates verticle down 3 ship
if random_num3ship == 1:
    verticleStart3length = random.randint(0,3)
    horizontalStart3length = random.randint(0,5)
    i = 0
    while((battleShipMap[verticleStart3length][horizontalStart3length] or battleShipMap[verticleStart3length+1][horizontalStart3length] or battleShipMap[verticleStart3length+2][horizontalStart3length]) == 1):
        verticleStart3length = random.randint(0,3)
        horizontalStart3length = random.randint(0,5)
    while i < 3:
        battleShipMap[verticleStart3length+i][horizontalStart3length] = 1
        i = i + 1
#this case creates horizontal across 3 ship
if random_num3ship == 2:
    verticleStart3length = random.randint(0,5)
    horizontalStart3length = random.randint(0,3)
    i = 0
    while((battleShipMap[verticleStart3length][horizontalStart3length] or battleShipMap[verticleStart3length][horizontalStart3length+1] or battleShipMap[verticleStart3length][horizontalStart3length+2]) == 1):
        verticleStart3length = random.randint(0,5)
        horizontalStart3length = random.randint(0,3)
    while i < 3:
        battleShipMap[verticleStart3length][horizontalStart3length+i] = 1
        i = i + 1

#random 2 ship generator
random_num3ship = random.randint(1,2)
#this case creates a verticle down 2 ship
if random_num3ship == 1:
    verticleStart2length = random.randint(0,4)
    horizontalStart2length = random.randint(0,5)
    i = 0
    while((battleShipMap[verticleStart2length][horizontalStart2length] or battleShipMap[verticleStart2length+1][horizontalStart2length]) == 1):
        verticleStart2length = random.randint(0,4)
        horizontalStart2length = random.randint(0,5)
    while i < 2:
        battleShipMap[verticleStart2length+i][horizontalStart2length] = 1
        i = i + 1
#this case creates horizontal across 2 ship
if random_num3ship == 2:
    verticleStart2length = random.randint(0,5)
    horizontalStart2length = random.randint(0,4)
    i = 0
    while((battleShipMap[verticleStart2length][horizontalStart2length] or battleShipMap[verticleStart2length][horizontalStart2length+1]) == 1):
        verticleStart2length = random.randint(0,5)
        horizontalStart2length = random.randint(0,4)
    while i < 2:
        battleShipMap[verticleStart2length][horizontalStart2length+i] = 1
        i = i + 1

#listen for and accept new connection(s), code waits here
serverSocket.listen(1)
connection, addr = serverSocket.accept()

#this splits the string for all possible guesses 1-6, did not account for error on the user end in this program
nums = 123456

#while running loop that checks if the map for hits and misses, and sends response back
while True:
    userGuess = int(connection.recv(1024).decode())
    userGuess = list(str(userGuess))
    if(battleShipMap[int(userGuess[0])-1][int(userGuess[1])-1] == 1):
        connection.send("HIT".encode())
    else:
        connection.send("MISS".encode())
    