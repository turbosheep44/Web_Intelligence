import re
import string
from os import listdir
from os.path import isfile, join
import json
import os
import re
import json
import sys

# Partitions the email into three sections, to, from and the email, data based on flags passed as arguments
def partitionEmail(path, toflag, fromflag, dataflag):
    with open(path, 'r+') as file:
        if(not(toflag) and not(fromflag) and not(dataflag)):
            return None, None, None

        fileSplit = file.read().partition("\n\n")
        inputFile = fileSplit[0]
        data = ""

        fromEmail = ""
        #to email includes CC and BCC
        toEmails = []
        #converting tabs separated emails into a single line
        headerClean = re.sub('([\s]*\n\t)', ' ', inputFile)

        for headerLine in headerClean.split("\n"):
            if(fromflag and headerLine.startswith("From:")):
                fromEmail = headerLine.split(" ")[1]

            if(toflag and (headerLine.startswith("To:") or headerLine.startswith("Cc:") or headerLine.startswith("Bcc:"))):
                
                toEmails = toEmailAdder(headerLine)

        if(not(toflag)):
            toEmails = None

        if(not(fromflag)):
            fromEmail = None

        if(not(dataflag)):
            data = None
        else:
            data = fileSplit[2]
            
        return toEmails, fromEmail, data

# Method that attempts to find the email of a particular person given their inbox, by finding
# the unique email that appears in the 'To:' section of the header
def getEmailFromInbox(rootpath):
    inboxList = os.listdir(rootpath+'/inbox')
    distinctEmails = set()
    for path in inboxList:
        # with open(rootpath+'/inbox/'+path, 'r+') as file:
        toEmails, _ , _ = partitionEmail(rootpath+'/inbox/'+path, True, False, False)

        # checking if the email is distinct
        if(len(distinctEmails) == 0):
            distinctEmails = set(toEmails)
        else:
            common = getCommon(distinctEmails, toEmails)
            if(len(common) == 1):
                for item in common:
                    return item
            else:
                distinctEmails = common

    return -1

# Takes a list of emails and formats them correctly
def toEmailAdder(headerLine):
    returnList = headerLine.replace('<.', "").replace(">", "").replace(",", "").split(" ")[1:]
    pattern = re.compile("\w[\w.]*\w@[\w.]*")
    returnList = [cleanEmailString(email) for email in returnList if pattern.match(email)]
    return returnList

# A large number of emails had the string '.' appended to the front, this method removes
# returns the email without that prefix
def cleanEmailString(email):
    index = email.find("'.'")

    if( index != -1 ):
        index += 3
        email = email[index:]
    return email

# Returns the emails that are in common between two sets of emails
def getCommon(old, newEmails):
    return old.intersection(newEmails)

# It was found that some people had more than one folder, for example data/panus-s and data/phanis-s are attributed
# to the same person, thus we should only add emails to the accepted list of emails if they are have not already been added
def addIfNotDuplicate(email):
    if(email not in acceptedEmails):
        acceptedEmails.append(email)

# Strips the email header and email data for a particular email
def parseSaveMessage(path):
    toEmails, fromEmail, data = partitionEmail(path, True, True, True)
    aList = [email for email in toEmails if email in acceptedEmails]

    if(fromEmail in acceptedEmails and len(aList) > 0):
        refName = path.replace("/", "") + "H"           
        
        saveFile = open('tobesure3/'+ refName, 'w')
        message = data.replace('\n',  ' ')
        parsed_msg = message.lower().translate(str.maketrans('', '', string.punctuation))
        parsed_msg = re.sub('\s+',' ',parsed_msg)

        saveFile.write(parsed_msg)
        saveFile.close()

        # Discard the case where the person is sending an email to themselves
        if(fromEmail in aList):
            aList.remove(fromEmail)

        # If the only user that the person is send an email to is themselves, then do nott consider
        # the email
        if(len(aList) > 0):
            for person in aList:
                if(person not in users_data ):
                    users_data[person] = {}
                    users_data[person]["sent"] = []
                    users_data[person]["received"] = []

                users_data[person]["received"].append(refName)    

            #first we will save the file
            if(fromEmail not in users_data):
                users_data[fromEmail] = {}
                users_data[fromEmail]["sent"] = []
                users_data[fromEmail]["received"] = []
                
            users_data[fromEmail]["sent"].append(refName)


        

if __name__ == "__main__":
    # attempts to find the emails which should be accepted for a particular folder by finding the path of
    # an email within the folder's sent directory, which would point to the unique email by reading the 'From' heading
    sentList = ['sent', '_sent_mail', 'sent_items']
    notFound = []
    acceptedPaths = []
    dirs = os.listdir('data/')
    for folder in dirs:
        for s in sentList:
            if(os.path.isdir('data/'+folder+'/'+s)):
                acceptedPaths.append('data/'+folder+'/'+s)
                break

            # for some cases, it was found that the sent folder is found within a subfolder under the person's name
            # for ex: instead of doe-j/_sent_mail, the user would have doe-j/john-doe/_sent_mail
            subFolder = os.listdir('data/'+folder)[0]
            if(os.path.isdir('data/'+folder+'/'+subFolder+'/'+s)):
                acceptedPaths.append('data/'+folder+'/'+subFolder+'/'+s)
                break
        else:   
            # if the folder does not have a sent directory, attempt to find the folder's email using
            # a different heuristic
            notFound.append('data/'+folder)

    # reads the first email within the sent directory of the folder, and finds the from heading
    acceptedEmails = []
    for person in acceptedPaths:
        with open(person + '/1_', 'r') as lines:
            for line in lines:
                if(line.startswith("From:")):
                    email = line.partition(":")[2].strip()
                    addIfNotDuplicate(email)
                    break

    # For emails with no sent folder, their email will be extracted from the inbox. Since there is no guarantee
    # that emails in the 'To:' section of an email header are unique, the method will iterate through all emails in the inbox
    # and attempt to find the email that appears in every one
    for email in notFound:
        retVal = getEmailFromInbox(email)
        if(retVal != -1):
            addIfNotDuplicate(email)
            break
    
    
    users_data = {}
    with open("email_paths.txt", "r") as allPaths:
        emailCounter = 0
        for path in allPaths:
            path = path.strip()
            print(str(emailCounter) + " - "  + path)
            parseSaveMessage(path)
            emailCounter += 1

        for person in users_data:
            weight = len(users_data[person]["sent"]) + len(users_data[person]["received"])
            users_data[person]["weight"] = weight

        f =  json.dumps(users_data,sort_keys=True, indent=4)

        with open("ching.json", "w") as outFile:
            outFile.write(f)
