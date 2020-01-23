from json import load as load_json
from json import dumps as json_dumps
from sys import argv as cmd_args

# load the metadata file
with open(f"{cmd_args[1]}", "r") as input_file:
    metadata = load_json(input_file)

# for each person, add the aliases to their node_data
for person in metadata:
    with open(f"{cmd_args[2]}/node_data/{metadata[person]['id']}.json", "r") as person_data_file:
        person_data = load_json(person_data_file)
    person_data["aliases"] = metadata[person]["aliases"]

    # rewrite the file
    with open(f"{cmd_args[2]}/node_data/{metadata[person]['id']}.json", "w") as person_data_file:
        print(json_dumps(person_data), file=person_data_file)
