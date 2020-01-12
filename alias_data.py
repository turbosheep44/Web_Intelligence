from json import load as load_json
from json import dumps as json_dumps


# load the metadata file
with open("metadata.json", "r") as input_file:
    metadata = load_json(input_file)

# for each person, add the aliases to their node_data
for person in metadata:
    with open(f"output_json/node_data/{metadata[person]['id']}.json", "r") as person_data_file:
        person_data = load_json(person_data_file)
    person_data["aliases"] = metadata[person]["aliases"]

    # rewrite the file
    with open(f"output_json/node_data/{metadata[person]['id']}.json", "w") as person_data_file:
        print(json_dumps(person_data), file=person_data_file)
