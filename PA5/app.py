
from flask import Flask,request
import random
import datetime

#read in funfacts txt
facts = []
addBack = []
f = open('facts.csv','r', encoding='utf-8')
for i in f:
    i = i.replace("\n", "")
    i = i.replace('"', "")
    facts.append(i)
f.close()
#flask
app = Flask(__name__)

@app.route('/fact')
def fact():
    j= 0 
    printStr = ""
    tempFact = facts
    i = int(request.headers['Amount'])
    while (j < i):
        randChoice = random.choice(tempFact)
        printStr = str(randChoice) + "\n\n" + printStr
        tempFact.remove(str(randChoice))
        addBack.append(str(randChoice))
        j = j + 1
    j= 0
    while (j < i):
        randChoice = random.choice(addBack)
        facts.append(randChoice)
        addBack.remove(str(randChoice))
        j = j + 1
    return "\n" + printStr

@app.route('/info')
def info():
    current_time = str(datetime.datetime.now())
    userAgent = str(request.user_agent)
    method = str(request.method)
    printStr = "\n" + "Time: " + current_time + "\n" + "User Agent: " + userAgent + "\n" + "Tranmission type: " + method + "\n"
    return printStr

if __name__ == '__main__':
    app.run()
