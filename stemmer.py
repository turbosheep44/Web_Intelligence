from stemming.porter2 import stem

def removeStopwordsAndStem(file):
    output = ""
    fileRead = open(file , "r")
    stopListLines = open("stopwords.txt" , "r")
    stopList = {}
    for line in stopListLines:
        stopList[line] = 0

    for line in fileRead:
        words = line.split()
        for word in words:
            if(word not in stopList):
                output += str(stem(word)) + " "

    fileRead.close()

    save = open(file, "r+")
    save.seek(0)
    save.wrrite(output)
    save.truncate()

    save.close()
 
 


