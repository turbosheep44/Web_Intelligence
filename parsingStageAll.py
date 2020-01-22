import re
import string
from os import listdir
from os.path import isfile, join
import json
import sys


def toEmailAdder(headerLine):
    returnList = headerLine.replace('<.', "").replace(">", "").replace(",", "").split(" ")[1:]
    pattern = re.compile("\w[\w.]*\w@[\w.]*")
    returnList = [cleanEmailString(email) for email in returnList if pattern.match(email)]
    return returnList

def cleanEmailString(email):
    index = email.find("'.'")

    if( index != -1 ):
        index += 3
        email = email[index:]
    return email

users_data = {}

def parseSaveMessage(path, emailCounter):
    with open(path, 'r+') as file:
        inputFile = file.read().partition("\n\n")
        data = inputFile[2]

        fromEmail = ""
        #to email includes CC and BCC
        toEmail = []
        #converting tabs separated emails into a single line
        headerClean = re.sub('([\s]*\n\t)', ' ', inputFile[0] )

        for headerLine in headerClean.split("\n"):
            if(headerLine.startswith("From:")):
                fromEmail = headerLine.split(" ")[1]
            if(headerLine.startswith("To:") or headerLine.startswith("Cc:") or headerLine.startswith("Bcc:")):
                toEmail = toEmailAdder(headerLine)
                
        refName = path.replace("/", "") + "H"
        
        saveFile = open('largeUnstemmed/'+ refName, 'w')
        message = data.replace('\n',  ' ')
        parsed_msg = message.lower()
        parsed_msg = re.sub('\s+',' ',parsed_msg)

        saveFile.write(parsed_msg)
        saveFile.close()
        
        #first we will save the file
        
        if( fromEmail not in users_data ):
            users_data[fromEmail] = {}
            users_data[fromEmail]["sent"] = []
            users_data[fromEmail]["received"] = []
        
        users_data[fromEmail]["sent"].append(refName)

        for person in toEmail:
            if( person not in users_data ):
                users_data[person] = {}
                users_data[person]["sent"] = []
                users_data[person]["received"] = []
            
            users_data[person]["received"].append(refName)
        

allPaths = open("email_paths.txt", "r")


def progressBar(value, endvalue, bar_length=20):

    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()

emailCounter = 0
for path in allPaths:
    path = path.strip()
    progressBar(emailCounter, 279012, 20)
    parseSaveMessage(path, emailCounter)
    emailCounter += 1

for  person in users_data:
    users_data[person]["weight"] = len(users_data[person]["sent"]) + len(users_data[person]["received"])

f =  json.dumps(users_data,sort_keys=True, indent=4)

outFile = open("original_metadata_big.json", "w")
outFile.write(f)
outFile.close()
allPaths.close()