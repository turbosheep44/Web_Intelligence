from json import dumps as json_dumps
from json import load as load_json
from sys import argv as cmd_args

# read the metadata json file
with open(cmd_args[1]) as json_file:
    data = load_json(json_file)

# remove all those whose weight is not in the top 150
users_to_keep = []
for user in data.keys():
    position = 0
    while position < len(users_to_keep) and data[users_to_keep[position]]["weight"] < data[user]["weight"]:
        position += 1
    users_to_keep.insert(position, user)
    users_to_keep = users_to_keep[-300:]

data = {user: data[user] for user in users_to_keep}
# for x in data:
#     print(x, data[x]["weight"])

# record a numberical id for each user
for index, name in enumerate(data.keys()):
    data[name]["id"] = index


# re-write metadata file
with open(cmd_args[2], 'w') as json_file:
    print(json_dumps(data), file=json_file)
