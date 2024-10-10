# Oliver Gough CSCI 466 program 2 9/24/2024

#---------------------------------------------------------Functions---------------------------------------------------------
#compares the prob of a curruption to a random number where if the rand < currption % it becomes currpted 
def randomCurruption(curruption_probability):
    compare_probability = random.randint(0, 100)
    if(compare_probability > (curruption_probability*100)):
        return True
    else:
        return False

#makes singular message packet
def createMessage(message, j, curruption_probability):
    return Packet(j, randomCurruption(curruption_probability), 3, maxSegmentSize, message)

#Creates NAK
def createNAK():
    print("Sending a NAK back")
    return Packet(0, True, 2, 0 ,"")
    
#Creates ACK
def createACK(curruption_probability):
    ack = Packet(0, randomCurruption(curruption_probability), 1, 0 ,"")
    if(ack.getChecksum() == False):
        print("Sending currupted ACK")
    else:
        print("Sending valid ACK")
    return ack

#prints out contents of current packet
def printSendingPacket(currentPacket):
    if(currentPacket.getChecksum() == False):
        print("\nSending currpted packet:")
    else:
        print("\nSending an ok packet:")
    print("-Sequence Num: " + str(currentPacket.getSequenceNum()))
    print("-Checksum: " + str(currentPacket.getChecksum()) + "\t\t (False = Currupted, True = Not Currupted)")
    print("ACK or NAK: " + str(currentPacket.getAckOrNak())+ "\t\t (1 = ACK, 2 = NAK, 3 = Message)")
    print("Message: " + str(currentPacket.getMessage()))
    print("Length: " + str(currentPacket.getLength()))
    return

#prints out contents of current packet
def printReceivedPacket(currentPacket):
    print("\nRecieved")
    print("-Sequence Num: " + str(currentPacket.getSequenceNum()))
    print("-Checksum: " + str(currentPacket.getChecksum()) + "\t\t (False = Currupted, True = Not Currupted)")
    print("ACK or NAK: " + str(currentPacket.getAckOrNak())+ "\t\t (1 = ACK, 2 = NAK, 3 = Message)")
    print("Message: " + str(currentPacket.getMessage()))
    print("Length: " + str(currentPacket.getLength()))
    return

#-------------------------------------------------------Start of main--------------------------------------------------------
import socket
import random
import sys
import time
import pickle
from packet import Packet 

#client setup
port = int(sys.argv[1])
maxSegmentSize = int(sys.argv[2])
curruption_probability = float(sys.argv[3])
host = socket.gethostname()

#bind socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect( (host,port) )

#get user input
print("Enter a sentence")
message = input()

#break user imput based on segment size
message = [(message[i:i+maxSegmentSize]) for i in range(0, len(message), maxSegmentSize)]
print("Message Packets:")
print(message[:])

#send the packets
packetNum = 0
while(packetNum < len(message)):
    currptionFlag = False
    while(currptionFlag == False): #1st packet and if packet revieived is a nak
        currentMessage = createMessage(message[packetNum], packetNum, curruption_probability)
        printSendingPacket(currentMessage)
        clientSocket.send(pickle.dumps(currentMessage)) #send packet
        time.sleep(1)
        recievePacket = pickle.loads(clientSocket.recv(1024)) #need to unpickle and make it into packet object
        if((recievePacket.getAckOrNak() == 1)and(recievePacket.getChecksum() == True)): #checks if ACK and if not currupted 
            print("\nValid ACK recieved, moving on")
            currptionFlag = True
        elif(recievePacket.getAckOrNak() == 2):
            print("\nNAK recieved, retransmitting")
        elif(recievePacket.getChecksum() == False):
            print("\nCurrupted ACK recieved, retransmitting")
    packetNum = packetNum +1

#TODO this shit get translated file

#rebind socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect( (host,port+1) )

#recieve translated sentence
fullMessage = ""
recieved = False
while (recieved == False):
    currentPacket = pickle.loads(clientSocket.recv(1024))
    printReceivedPacket(currentPacket)
    if currentPacket.getChecksum() == False: #currupted message 
        clientSocket.send(pickle.dumps(createNAK())) #send nak
    else:#good data
        ack = createACK(curruption_probability)
        clientSocket.send(pickle.dumps(ack)) #send ack
        if(ack.getChecksum() == True):
            fullMessage = fullMessage + currentPacket.getMessage()
            if (fullMessage[len(fullMessage)- 1] == ("." or "?" or "!")): #checks last letter
                recieved = True #breaks out of loop

print("Full translated message: " + str(fullMessage))
