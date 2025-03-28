# Oliver Gough CSCI 466 program 2 9/24/2024

#---------------------------------------------------------Functions---------------------------------------------------------
#compares the prob of a curruption to a random number where if the rand < currption % it becomes currpted 
def randomCurruption(curruption_probability):
    compare_probability = random.randint(0, 100)
    if(compare_probability > (curruption_probability*100)):
        return True
    else:
        return False

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

#makes singular message packet
def createMessage(message, j, curruption_probability):
    return Packet(j, randomCurruption(curruption_probability), 3, maxSegmentSize, message)

#prints out contents of current packet
def printReceivedPacket(currentPacket):
    print("\nRecieved")
    print("-Sequence Num: " + str(currentPacket.getSequenceNum()))
    print("-Checksum: " + str(currentPacket.getChecksum()) + "\t\t (False = Currupted, True = Not Currupted)")
    print("ACK or NAK: " + str(currentPacket.getAckOrNak())+ "\t\t (1 = ACK, 2 = NAK, 3 = Message)")
    print("Message: " + str(currentPacket.getMessage()))
    print("Length: " + str(currentPacket.getLength()))
    return

#makes a list of the translated message and compares each letter to the capitalziation of input then joins list to string works ok
def perserveCapitalization(fullMessage, translatedMessage):
    x = 0
    t = list(translatedMessage)
    if(len(translatedMessage) < len(fullMessage)):
        for i in translatedMessage:
            if(fullMessage[x].upper() == fullMessage[x]):
                t[x] = t[x].upper()
            x = x+1
    else:
        for i in fullMessage:
            if(i.upper() == i):
                t[x] = t[x].upper()
            x = x+1
    return "".join(t)

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

#-------------------------------------------------------Start of main--------------------------------------------------------
import socket
import random
import sys
import pickle
import time
from packet import Packet 

#server setup
port = int(sys.argv[1]) #change this for more args
maxSegmentSize = int(sys.argv[2])
curruption_probability = float(sys.argv[3])
host = socket.gethostname()

#bind socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind( (host, port) )

#listen for and accept new connection(s), code waits here
serverSocket.listen(1)
connection, addr = serverSocket.accept()

#read in csv file of priate translations and creates a hash map
file = open('pirate.csv','r')
translationDict = {}
x = 0
for i in file:
    if (x == 0):
        splitLine = i.strip().split(",")
        i =  splitLine[0]
        translationDict.update({i[3:]:splitLine[1]})
    else:
        splitLine = i.strip().split(",")
        translationDict.update({splitLine[0]:splitLine[1]})
    x = x+1

fullMessage = ""
recieved = False

#starts to recieve the messages to translate
while (recieved == False):
    currentPacket = pickle.loads(connection.recv(1024))
    printReceivedPacket(currentPacket)
    if currentPacket.getChecksum() == False: #currupted message 
        connection.send(pickle.dumps(createNAK())) #send nak
    else:#good data
        ack = createACK(curruption_probability)
        connection.send(pickle.dumps(ack)) #send ack
        if(ack.getChecksum() == True):
            fullMessage = fullMessage + currentPacket.getMessage()
            if ((fullMessage[len(fullMessage)- 1] == '.') or (fullMessage[len(fullMessage)- 1] == '?') or (fullMessage[len(fullMessage)- 1] == '!')): #checks last letter
                recieved = True #breaks out of loop

#translates message by checking if in hashmap then removes the space and adds back the punctuatuion
print("\nTranslating\nMessage recieved from client: " + "".join(fullMessage))
print("\n")
print(translationDict)
print("\n")
translatedMessage = ""
i = 0
messageToTranslate = fullMessage[:-1]
words = messageToTranslate.split()
while(i < len(words)):
    if (words[i].lower() not in translationDict): #element is not in hashmap
        translatedMessage = translatedMessage + " " + words[i]
    else:  #element is in hashmap
        translatedMessage = translatedMessage + " " + translationDict.get(words[i].lower())
    i = i + 1
translatedMessage = translatedMessage[1:] + fullMessage[len(fullMessage) -1] #full message
translatedMessage = perserveCapitalization(fullMessage, translatedMessage) #fixes capitalization
print("Translated message to send: " + translatedMessage)

#rebind socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind( (host, port+1) )
serverSocket.listen(1)
connection, addr = serverSocket.accept()

#send translated packets
translatedMessage = [(translatedMessage[i:i+maxSegmentSize]) for i in range(0, len(translatedMessage), maxSegmentSize)]
packetNum = 0
while(packetNum < len(translatedMessage)):
    currptionFlag = False
    while(currptionFlag == False): #1st packet and if packet revieived is a nak
        currentMessage = createMessage(translatedMessage[packetNum], packetNum, curruption_probability)
        printSendingPacket(currentMessage)
        connection.send(pickle.dumps(currentMessage)) #send packet
        time.sleep(3)
        recievePacket = pickle.loads(connection.recv(1024)) #need to unpickle and make it into packet object
        if((recievePacket.getAckOrNak() == 1)and(recievePacket.getChecksum() == True)): #checks if ACK and if not currupted 
            print("\nValid ACK recieved, moving on")
            currptionFlag = True
        elif(recievePacket.getAckOrNak() == 2):
            print("\nNAK recieved, retransmitting")
        elif(recievePacket.getChecksum() == False):
            print("\nCurrupted ACK recieved, retransmitting")
    packetNum = packetNum + 1
print("\nFile sent! End of server program.\n")
