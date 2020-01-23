
OUTPUT_FOLDER="output_json_test"
ORIGINAL_METADATA_JSON="original_metadata.json"
FILTERED_METADATA_JSON="metadata.json"
MESSAGES_FOLDER="messages_fancy_filter"

mkdir -p $OUTPUT_FOLDER

python3 filter.py $ORIGINAL_METADATA_JSON $FILTERED_METADATA_JSON
python3 documents.py $FILTERED_METADATA_JSON $OUTPUT_FOLDER
python3 graph_facts.py $OUTPUT_FOLDER
python3 tf_idf.py $FILTERED_METADATA_JSON $OUTPUT_FOLDER $MESSAGES_FOLDER
python3 pagerank.py $FILTERED_METADATA_JSON $OUTPUT_FOLDER
python3 alias_data.py $FILTERED_METADATA_JSON $OUTPUT_FOLDER

# /messages_big original_metadata_big.json
# /messages_small original_metadata_small.json