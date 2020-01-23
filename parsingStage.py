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
import numpy as np
import sys

# assumes the directory 'data' exists and contains all the emails

# outputs email message data to folder called smallUnstemmed
# outputs json containing references to original_metadata_small
# outputs json used internally to accepted_emails.json

# Partitions the email into three sections, to, from and the email, data based on flags passed as arguments


def partitionEmail(path, toflag, fromflag, dataflag):

    # encoding argument is used since there are non-utf 8 characters present in the dataset
    with open(path, 'r+',  encoding='windows-1252') as file:
        if(not(toflag) and not(fromflag) and not(dataflag)):
            return None, None, None

        fileSplit = file.read().partition("\n\n")
        inputFile = fileSplit[0]
        data = ""

        fromEmail = ""
        # to email includes CC and BCC
        toEmails = []
        # converting tabs separated emails into a single line
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
        toEmails, _, _ = partitionEmail(
            rootpath+'/inbox/'+path, True, False, False)

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
    returnList = headerLine.replace('<.', "").replace(
        ">", "").replace(",", "").split(" ")[1:]
    pattern = re.compile("\w[\w.]*\w@[\w.]*")
    returnList = [cleanEmailString(email)
                  for email in returnList if pattern.match(email)]
    return returnList

# A large number of emails had the string '.' appended to the front, this method removes
# returns the email without that prefix


def cleanEmailString(email):

    index = max(email.find("'.'"), email.find("<."))

    if(index != -1):
        index += 3
        email = email[index:]
    return email.replace('>', '')

# Returns the emails that are in common between two sets of emails


def getCommon(old, newEmails):
    return old.intersection(newEmails)

# It was found that some people had more than one folder, for example data/panus-s and data/phanis-s are attributed
# to the same person, thus we should only add emails to the accepted list of emails if they are have not already been added


def addIfNotDuplicate(email):
    if(email not in acceptedEmails):
        acceptedEmails.add(email)

# Strips the email header and email data for a particular email


def parseSaveMessage(path):
    toEmails, fromEmail, data = partitionEmail(path, True, True, True)
    # print(toEmails)
    aList = [email for email in toEmails if email in acceptedEmails]
    # print(aList)

    if(fromEmail in acceptedEmails and len(aList) > 0):
        refName = path.replace("/", "") + "H"

        saveFile = open(f'{sys.argv[1]}/' + refName, 'w')
        message = data.replace('\n',  ' ')
        parsed_msg = message.lower()
        parsed_msg = re.sub('\s+', ' ', parsed_msg)

        saveFile.write(parsed_msg)
        saveFile.close()
        # Discard the case where the person is sending an email to themselves
        if(fromEmail in aList):
            aList.remove(fromEmail)

        # If the only user that the person is send an email to is themselves, then do nott consider
        # the email
        if(len(aList) > 0):
            for person in aList:
                if(inverseAccepted[person] not in users_data):
                    users_data[inverseAccepted[person]] = {}
                    users_data[inverseAccepted[person]]["sent"] = []
                    users_data[inverseAccepted[person]]["received"] = []

                users_data[inverseAccepted[person]]["received"].append(refName)

            # first we will save the file
            if(inverseAccepted[fromEmail] not in users_data):
                users_data[inverseAccepted[fromEmail]] = {}
                users_data[inverseAccepted[fromEmail]]["sent"] = []
                users_data[inverseAccepted[fromEmail]]["received"] = []

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
            m1m = levenshtein(emailPart, s2)
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
        print('Folder: ' + folder + ' contains email which is already associated with: ' +
              inverseAccepted[email.strip()])

    addToPairedCounter(email.strip())


def addToNotPaired(email):
    if(email not in notPaired):
        notPaired[email] = 1
    else:
        notPaired[email] += 1


def addToPairedCounter(email):
    if(email not in pairedCount):
        pairedCount[email] = 1
    else:
        pairedCount[email] += 1


if __name__ == "__main__":
    # attempts to find the emails which should be accepted for a particular folder by finding the path of
    # an email within the folder's sent directory, which would point to the unique email by reading the 'From' heading
    if(not os.path.isfile('accepted_emails_small.json')):
        sentList = ['sent', '_sent_mail', 'sent_items']
        notPaired = {}
        pairedCount = {}
        alias_data = {}
        total = 0
        acceptedEmails = set()
        inverseAccepted = {}
        dirs = os.listdir('data/')
        for folder in dirs:
            best = ""
            bestL = math.inf
            strippedsurname = folder.split('-')[0]
            subfolderused = False
            for s in sentList:
                if(os.path.isdir('data/'+folder+'/'+s)or os.path.isdir('data/'+folder+'/'+os.listdir('data/'+folder)[0]+'/'+s)):
                    if(os.path.isdir('data/'+folder+'/'+os.listdir('data/'+folder)[0]+'/' + s)):
                        folder += '/' + os.listdir('data/'+folder)[0]
                        subfolderused = True
                    files = os.listdir('data/'+folder+'/'+s)
                    for fileno in files:
                        if(not os.path.isdir('data/'+folder+'/'+s+'/'+fileno)):

                            with open('data/'+folder+'/'+s+'/'+fileno,  encoding='windows-1252') as filedata:
                                fileSplit = filedata.read().partition("\n\n")
                                inputFile = fileSplit[0]

                                for line in inputFile.split('\n'):
                                    if(line.startswith("From:")):
                                        email = line.partition(":")[2].strip()
                                        email = cleanEmailString(email)
                                        if(strippedsurname in email or string_dist(email.split("@")[0], strippedsurname) <= 1):
                                            addToFolder(
                                                folder, email, subfolderused)
                                            bestL = -1
                                        else:
                                            addToNotPaired(email)
                                            levD = string_dist(
                                                email.split("@")[0], strippedsurname)
                                            if(levD < bestL):
                                                best = email
                                                bestL = levD

            if(os.path.isdir('data/'+folder+'/inbox')):
                inboxList = os.listdir('data/'+folder+'/inbox')
                distinctEmails = set()
                for path in inboxList:
                    if(os.path.isdir('data/'+folder+'/inbox/'+path)):
                        continue
                    toEmails, _, _ = partitionEmail(
                        'data/'+folder+'/inbox/'+path, True, False, False)
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
                                else:
                                    addToNotPaired(email)
                                    if(bestL != -1):
                                        levD = string_dist(
                                            item.split("@")[0], strippedsurname)
                                        if(levD < bestL):
                                            best = item
                                            bestL = levD

                                distinctEmails = {}
                        else:
                            distinctEmails = common

            if(bestL < math.inf and bestL != -1):
                addToFolder(folder, best, subfolderused)
                del notPaired[best]
                print('Adding the closest email ' +
                      best + ' for folder ' + folder)

            if(folder in alias_data and len(alias_data[folder]) != 0):
                print(alias_data[folder])
                print()
            # setting the alias list for that person

        total = sum(list(pairedCount.values()))
        average = total/len(pairedCount)

        lowerBound = average/6

        counter = 0
        print("The following emails were deemed important enough to keep:")
        for key in notPaired:
            if(lowerBound <= notPaired[key]):
                print(key + ' passses. ' + str(lowerBound) +
                      ' <= ' + str(notPaired[key]))
                addToFolder(key.partition("@")[0], key, False)
                counter += 1

        f = json.dumps(users_data, sort_keys=True, indent=4)

        with open("accepted_emails_small.json", "w") as outFile:
            outFile.write(acceptedEmails)

    else:
        with open('accepted_emails_small.json', 'r') as g:
            alias_data = json.load(g)
            acceptedEmails = list(
                itertools.chain.from_iterable(alias_data.values()))

            inverseAccepted = {}
            for key in alias_data:
                for value in alias_data[key]:
                    inverseAccepted[value] = key

    users_data = {}
    with open("email_paths.txt", "r") as allPaths:
        emailCounter = 0
        for path in allPaths:
            path = path.strip()
            print(str(emailCounter) + " - " + path)
            parseSaveMessage(path)
            emailCounter += 1
        # print(alias_data)

        for person in users_data:
            # setting the weight for that person
            weight = len(users_data[person]["sent"]) + \
                len(users_data[person]["received"])
            users_data[person]["weight"] = weight
            users_data[person]["aliases"] = alias_data[person]

        f = json.dumps(users_data, sort_keys=True, indent=4)

        with open(f"{sys.argv[2]}", "w") as outFile:
            outFile.write(f)
