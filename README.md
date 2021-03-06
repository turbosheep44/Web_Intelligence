# Initialising the Environment

In order to install the correct dependencies in a virtual environment use the following commands:

```
 $ python3 -m venv env
 $ source env/bin/activate
 $ pip install -r requirements.txt
```

# Running the Program

To create the data folders from scratch, run the scripts `big.sh` and `small.sh`. It is assumed that the maildir exists in the same folder as the scripts - this folder should be named `data`. Then open the server with `python3 server.py`.

The scripts are run in the following forder to create the data:
 - `parsingStage{All}.py [output unstemmed folder] [output metadata]` (extract metadata and separate body)
 - `stemmer.py [input directory] [output directory]` (clean email bodies)
 - `filter.py [input json] [output json (metadata)]` (filter any unwanted users and give a numerical ID to each user)
 - `documents.py [metadata json input] [output folder]` (creates documents for each distinct user pair)
 - `graph_facts.py [input/output folder]` (gets all the facts about graph and nodes)
 - `tf_idf.py [metadata json input] [input/output folder] [messages directory]` (gets all the node and edge word cloud data)
 - `pagerank.py [metadata json input] [input/output folder]` (calculates pagerank data for each node and saves it)
 - `alias_data.py [metadata json input] [input/output folder]` (adds alias data to the node data files - only applicable for filtered data set)
 - `server.py` (serve the web dashboard)

# Files

`graph.json`: data for D3 & used by `graph_facts.py`

`node_data/{id}.json` : information about a particular node
`tf_idf_nodes/{id}.json` : TF.IDF data for a word cloud for this node
`tf_idf_edges/{id}_{id}.json` : TF.IDF data for a word cloud for this edge

```json
{
    "name" : "joe.borg@enron.com",
    "weight" : 7,
    "neighbour_count" : 4,
    "clustering_coefficient" : 0.333333333,
    "eccentricity" : 4,
    "average_path_distance" : 2.4575
}
```
