class Packet:  
      
    def __init__(self, sequenceNum, checksum, ackOrNak, length, message):
        self.sequenceNum = sequenceNum
        self.checksum = checksum #true = good, False = currupted
        self.ackOrNak = ackOrNak #1 = ack, 2 = nak, 3 = message
        self.length = length
        self.message = message

    def getChecksum(self):
        return self.checksum
    
    def getSequenceNum(self):
        return self.sequenceNum
    
    def getAckOrNak(self):
        return self.ackOrNak
    
    def getMessage(self):
        return self.message  
    
    def getLength(self):
        return len(self.message)
    
