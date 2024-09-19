# Oliver Gough CSCI 466 program 1 client battleship 9/11/2024

import socket
import sys

#server setup
port = int(sys.argv[1])
host = socket.gethostname()

#bind socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect( (host,port) )

#initalize variables to use
numOfGuesses = 0
sunkAllShips = False
hitCounter = 0
hitMissMap = [["?","?","?","?","?","?"],["?","?","?","?","?","?"],["?","?","?","?","?","?"],["?","?","?","?","?","?"],["?","?","?","?","?","?"],["?","?","?","?","?","?"],]

#While loop to communicate with socket
while(not sunkAllShips):

#prompts user for input and prints our map
    for i in hitMissMap:
        print(i)
    userGuessRow = input("Enter row: ")
    userGuessColumn = input("Enter column: ")

#sends guess as a string of 2 nums 
    clientSocket.send((userGuessRow + userGuessColumn).encode())

#gets response from server and uses if statments to see the result
    response = clientSocket.recv(1024).decode()    
    print(response)
    userGuessRow =  int(userGuessRow) -1
    userGuessColumn = int(userGuessColumn) -1

#update the map accodingly and looks for win condtion, ie place an x nine time bc 4+3+2 = 9 
    if(response == "HIT"):
        numOfGuesses = numOfGuesses +1 
        if (hitMissMap[userGuessRow][userGuessColumn] != "X"):
            hitMissMap[userGuessRow][userGuessColumn] = "X"
            hitCounter = hitCounter + 1
        elif (hitMissMap[userGuessRow][userGuessColumn] == "X"):
            print("You already hit that spot")
    if(response == "MISS"):
        numOfGuesses = numOfGuesses +1 
        hitMissMap[userGuessRow][userGuessColumn] = "O"

#win condition met so we print out the map and num of guesses
    if(hitCounter == 9):
        for i in hitMissMap:
            print(i)
        print("Game over!")
        print("It took you " + str(numOfGuesses) + " guesses")
        clientSocket.send(("77").encode())
        sunkAllShips = True