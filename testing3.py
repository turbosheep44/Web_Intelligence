import re
import string
from os import listdir
from os.path import isfile, join
import json
import os
import re
import json
import sys
import math
import itertools

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

    index = max(email.find("'.'"), email.find("<."))

    if( index != -1 ):
        index += 3
        email = email[index:]
    return email.replace('>', '')

# Returns the emails that are in common between two sets of emails
def getCommon(old, newEmails):
    return old.intersection(newEmails)

# It was found that some people had more than one folder, for example data/panus-s and data/phanis-s are attributed

# Strips the email header and email data for a particular email
def parseSaveMessage(path):
    toEmails, fromEmail, data = partitionEmail(path, True, True, True)
    
    refName = path.replace("/", "") + "H"           
    
    saveFile = open('DIR/'+ refName, 'w')
    message = data.replace('\n',  ' ')
    parsed_msg = message.lower().translate(str.maketrans('', '', string.punctuation))
    parsed_msg = re.sub('\s+',' ',parsed_msg)

    saveFile.write(parsed_msg)
    saveFile.close()

    # Discard the case where the person is sending an email to themselves
    if(fromEmail in toEmails):
        toEmails.remove(fromEmail)

    # If the only user that the person is send an email to is themselves, then do nott consider
    # the email
    if(len(toEmails) > 0):
        for person in toEmails:
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
            
        users_data[inverseAccepted[fromEmail]]["sent"].append(refName)
        


memo = {}
def levenshtein(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    cost = 0 if s[-1] == t[-1] else 1
       
    i1 = (s[:-1], t)
    if not i1 in memo:
        memo[i1] = levenshtein(*i1)
    i2 = (s, t[:-1])
    if not i2 in memo:
        memo[i2] = levenshtein(*i2)
    i3 = (s[:-1], t[:-1])
    if not i3 in memo:
        memo[i3] = levenshtein(*i3)
    res = min([memo[i1]+1, memo[i2]+1, memo[i3]+cost])
    
    return res

def string_dist(s1, s2):
    
    minimum = math.inf
    memo = {}
    if("." in s1):
        emailSplit = s1.split(".")
        for emailPart in emailSplit:
            # print('between ' + emailPart + ' and  '+ s2)
            m1m = levenshtein(emailPart, s2)
            # print(minimum , ' and ' , m1m)
            minimum = min(minimum, m1m)
    else:
        minimum = levenshtein(s1, s2)


    return minimum
    


def addEmailUnderAlias(alias, email):
    alias_stripped = alias.strip()
    email_stripped = email.strip()

    if(alias_stripped not in alias_data):
        alias_data[alias_stripped] = []
        # print('added alias ' + alias_stripped)
    
    if(email_stripped not in alias_data[alias_stripped]):
        alias_data[alias_stripped].append(email_stripped)

def addToFolder(folder, email, subfolder):
    tempfolder = folder
    if(subfolder):

        tempfolder = folder.partition('/')[0]
    
    if(email not in acceptedEmails):
        addEmailUnderAlias(tempfolder, email)
        acceptedEmails.add(email.strip())
        inverseAccepted[email.strip()] = tempfolder
    elif(folder != inverseAccepted[email.strip()]):
        print('This guy is trying to cheat ' + folder + ' copying ' + inverseAccepted[email.strip()])

if __name__ == "__main__":
    # attempts to find the emails which should be accepted for a particular folder by finding the path of
    # an email within the folder's sent directory, which would point to the unique email by reading the 'From' heading
    if(not os.path.isfile('testing100s.json')):
        sentList = ['sent', '_sent_mail', 'sent_items']
        notFound = []
        # acceptedPaths = []
        alias_data = {}
        total = 0
        acceptedEmails = set()
        inverseAccepted = {}
        dirs = os.listdir('data/')
        for folder in dirs:
            # print(folder)
            # personslist = []
            best = ""
            bestL = math.inf
            strippedsurname = folder.split('-')[0]
            subfolderused = False
            for s in sentList:
                if(os.path.isdir('data/'+folder+'/'+s)or os.path.isdir('data/'+folder+'/'+os.listdir('data/'+folder)[0]+'/'+s)):
                    if(os.path.isdir('data/'+folder+'/'+os.listdir('data/'+folder)[0]+'/' +s)):
                        folder += '/' +os.listdir('data/'+folder)[0]
                        subfolderused = True
                    # acceptedPaths.append('data/'+folder+'/'+s)
                    # personslist.append('data/'+folder+'/'+s)
                    files = os.listdir('data/'+folder+'/'+s)
                    for fileno in files:
                        if(not os.path.isdir('data/'+folder+'/'+s+'/'+fileno)):
                            with open('data/'+folder+'/'+s+'/'+fileno) as filedata:
                                fileSplit = filedata.read().partition("\n\n")
                                inputFile = fileSplit[0]
                                
                                for line in inputFile.split('\n'):
                                    if(line.startswith("From:")):
                                        email = line.partition(":")[2].strip()
                                        email = cleanEmailString(email)
                                        if(strippedsurname in email or string_dist(email.split("@")[0], strippedsurname) <= 1):
                                            addToFolder(folder, email, subfolderused)
                                            bestL = -1
                                            
                                        else:
                                            levD = string_dist(email.split("@")[0], strippedsurname)
                                            if(levD < bestL):
                                                best = email
                                                bestL = levD
                                        
            if(os.path.isdir('data/'+folder+'/inbox')): 
                inboxList = os.listdir('data/'+folder+'/inbox')
                distinctEmails = set()
                for path in inboxList:
                    if(os.path.isdir('data/'+folder+'/inbox/'+path)):
                        continue
                    toEmails, _ , _ = partitionEmail('data/'+folder+'/inbox/'+path, True, False, False)
                    if(len(distinctEmails) == 0):
                        distinctEmails = set(toEmails)
                    else:
                        common = getCommon(distinctEmails, toEmails)
                        if(len(common) == 1):
                            for item in common:
                                item = cleanEmailString(item)

                                if(strippedsurname in item or string_dist(item.split("@")[0], strippedsurname) <= 1):
                                    # print('adding ' + item +' from ' + 'data/'+folder+'/inbox/' + path)
                                    addToFolder(folder, item, False)

                                    bestL = -1
                                    # personslist.append(item.strip())
                                elif(bestL != -1):
                                    levD =  string_dist(item.split("@")[0], strippedsurname)
                                    if(levD < bestL):
                                        best = item
                                        bestL = levD

                                
                                distinctEmails = {}
                        else:
                            distinctEmails = common
            
            if(bestL < math.inf and bestL != -1):
                addToFolder(folder, best, subfolderused)
                print('adding the least worst ' + best + ' for ' + folder)

            if(folder in alias_data and len(alias_data[folder]) != 0):
                print(alias_data[folder])
                print()

        f =  json.dumps(alias_data,sort_keys=True, indent=4)

        with open("testing100s.json", "w") as outFile:
            outFile.write(f)
            exit()
    else:
        with open('testing100s.json', 'r') as g:
            alias_data = json.load(g)
            acceptedEmails = list(itertools.chain.from_iterable(alias_data.values()))

            inverseAccepted = {}
            for key in alias_data:
                for value in alias_data[key]:
                    # inverseAccepted[value] = {}
                    inverseAccepted[value] = key
                    #

        # print('Current subtotal:  ' + str(total) +  ' emails')
            # # for some cases, it was found that the sent folder is found within a subfolder under the person's name
            # # for ex: instead of doe-j/_sent_mail, the user would have doe-j/john-doe/_sent_mail
            # subFolder = os.listdir('data/'+folder)[0]
            # if(os.path.isdir('data/'+folder+'/'+subFolder+'/'+s)):
            #     # acceptedPaths.append('data/'+folder+'/'+subFolder+'/'+s)
            #     personslist.append('data/'+folder+'/'+s)

        # else:   
        #     # if the folder does not have a sent directory, attempt to find the folder's email using
        #     # a different heuristic
        #     notFound.append('data/'+folder)

        # for person in personslist:
        #     personsemails = []
        #     with open(person + '/1_', 'r') as lines:
        #         for line in lines:
        #             if(line.startswith("From:")):
        #                 email = line.partition(":")[2].strip()
        #                 addIfNotDuplicate(email)
        #                 break

    # # reads the first email within the sent directory of the folder, and finds the from heading
    # acceptedEmails = []
    # for person in acceptedPaths:
    #     with open(person + '/1_', 'r') as lines:
    #         for line in lines:
    #             if(line.startswith("From:")):
    #                 email = line.partition(":")[2].strip()
    #                 addIfNotDuplicate(email)
    #                 break

    # For emails with no sent folder, their email will be extracted from the inbox. Since there is no guarantee
    # that emails in the 'To:' section of an email header are unique, the method will iterate through all emails in the inbox
    # and attempt to find the email that appears in every one
    # for email in notFound:
    #     retVal = getEmailFromInbox(email)
    #     if(retVal != -1):
    #         addIfNotDuplicate(email)
    #         break
    
    
    users_data = {}
    with open("email_paths.txt", "r") as allPaths:
        emailCounter = 0
        for path in allPaths:
            path = path.strip()
            print(str(emailCounter) + " - "  + path)
            parseSaveMessage(path)
            emailCounter += 1
        # print(alias_data)

        for person in users_data:
            # setting the weight for that person
            weight = len(users_data[person]["sent"]) + len(users_data[person]["received"])
            users_data[person]["weight"] = weight
            users_data[person]["aliases"] = alias_data[person]
            
            # setting the alias list for that person

        f =  json.dumps(users_data,sort_keys=True, indent=4)

        with open("finalfartin.json", "w") as outFile:
            outFile.write(f)
