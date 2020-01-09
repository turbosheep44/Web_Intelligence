import re
import string
from os import listdir
from os.path import isfile, join
import json

def toEmailAdder(headerLine):
    returnList =  headerLine.replace(',','').replace('\n',' ').strip().split(" ")[1:]
    returnList = [cleanEmailString(email) for email in returnList]
    # print(returnList)
    return returnList

def cleanEmailString(email):
    index = email.find("'.'")

    if (email.endswith(">")):
        email = email[:-1]

    if (email.startswith("<.")):
        email = email [2:]

    if( index != -1 ):
        index += 3
        email = email[index:]
    return email

users_data = {}

def parseSaveMessage(path, emailCounter):
    with open(path, 'r+') as file:
        inputFile = file.read().split("\n\n")
        data = " ".join(inputFile[1:])

        fromEmail = ""
        multilineTOList = False
        tempLineTotal = ""
        #to email includes CC and BCC
        toEmail = []
        la = inputFile[0].split("\n")
        #TO:DO change vriable la name
        for i, headerLine in enumerate(la):
            
            
            if(headerLine.startswith("From:")):
                fromEmail = headerLine.split(" ")[1]
            if(not (multilineTOList) and (headerLine.startswith("To:") or headerLine.startswith("Cc:") or headerLine.startswith("Bcc:"))):
                #check what the next line holds
                if(la[i+1].startswith("\t") and multilineTOList == False):
                    multilineTOList = True
                    # print ("sibt tab Yo haters)")
                    tempLineTotal += headerLine.strip() + " "
                elif(not(la[i+1].startswith("\t"))):
                    toEmail = toEmailAdder(headerLine)
            elif(multilineTOList):
                # print ("ntext line " + la[i+1])
                if( not(la[i+1].startswith("\t")) ):
                        tempLineTotal += headerLine.strip() + " "
                        # print("You yoyoyoy jien kont qieghed scannign u issa ha nieqaf ghax sibt li, li jmiss ma jibdiex btab")
                        toEmail = toEmailAdder(tempLineTotal)
                        tempLineTotal = ""
                        multilineTOList = False
                        # print(toEmail)
                else:
                    tempLineTotal += headerLine.strip() + " "
                    



                

                
        refName = path.replace(", /", "") + "H"
        saveFile = open('messages/'+ refName, 'w+')
        message = data.replace('\n',  ' ')
        parsed_msg = message.lower().translate(str.maketrans('', '', string.punctuation))
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

emailCounter = 0
for path in allPaths:
    path = path.strip()
    print("FILE: " + path)
    parseSaveMessage(path, emailCounter)
    emailCounter += 1

for  person in users_data:
    users_data[person]["weight"] = len(users_data[person]["sent"]) + len(users_data[person]["received"])

f =  json.dumps(users_data,sort_keys=True, indent=4)

outFile = open("metadata.json", "w")
outFile.write(f)
outFile.close()
