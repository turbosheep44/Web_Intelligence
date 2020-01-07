from math import log as ln
from json import dumps as json_dumps
from json import load as load_json


# read the document_list json file
with open('document_list.json') as json_file:
    document_list = load_json(json_file)

# extract the two separate dictionaries (making conversions as necessary)
users = {user_name: int(document_list["users"][user_name])
         for user_name in document_list["users"]}
documents = {int(document_id): document_list["documents"][document_id]
             for document_id in document_list["documents"]}

# count the terms in each document
documents = {}
for filename in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]:
    with open("messages/" + filename, "r") as f:
        document = {}
        for line in f:
            for word in line.strip().split(" "):
                word = word.strip()
                document[word] = document.get(word, 0)+1

        documents[filename] = document
        print("{:2}".format(filename) + " : " + str(document))


def tf_idf(documents, word, searchDoc):
    # Term frequency (default 0)
    tf = documents[searchDoc].get(word, 0)

    # inverse document frequency
    number_of_documents = len(documents.keys())
    term_in_documents = 0
    for doc in documents:
        if word in documents[doc]:
            term_in_documents += 1

    idf = ln(number_of_documents/term_in_documents)
    return tf * idf


# calculate TF.IDF
searchDoc = "7"
print([tf_idf(documents, word, searchDoc) for word in documents[searchDoc]])
