from itertools import combinations
from json import dumps as json_dumps
from json import load as load_json


# list intersect
# given two lists, finds the common elements in O(n) time
def intersect(listA, listB):
    setA = set(listA)
    return [x for x in listB if x in setA]


# read the metadata json file
with open('metadata.json') as json_file:
    data = load_json(json_file)

# get a list of all the distinct user pairs
distinct_user_pairs = combinations(list(data.keys()), 2)

# record the bitwise representation value of each user
users_bitwise = {name: index for index, name in enumerate(list(data.keys()))}

# for each distinct user pair
#   one = userA.send intersect userB.received
#   two = userB.send intersect userA.received
#   document['AB'] = one union two
documents = {}
for user_pair in distinct_user_pairs:
    documents[1 << users_bitwise[user_pair[0]] | 1 << users_bitwise[user_pair[1]]] = \
        intersect(data[user_pair[0]]["sent"], data[user_pair[1]]["received"]) + \
        intersect(data[user_pair[1]]["sent"], data[user_pair[0]]["received"])


with open("document_list.json", "w") as output:
    print(json_dumps({"users": users_bitwise,
                      "documents": documents}, indent=4), file=output)
