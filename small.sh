OUTPUT_METADATA="original_metadata_small.json"
OUTPUT_FOLDER_UNSTEMMED="output_unstemmed_small"
OUTPUT_STEMMED="messages_small"

mkdir -p $OUTPUT_FOLDER_UNSTEMMED
mkdir -p $OUTPUT_STEMMED

#this is for the small one, will output a json and will populate a folder
python3 parsingStage.py $OUTPUT_FOLDER_UNSTEMMED $OUTPUT_METADATA
python3 stemmer.py $OUTPUT_FOLDER_UNSTEMMED $OUTPUT_STEMMED

##########################

OUTPUT_FOLDER="output_json_small"
FILTERED_METADATA_JSON="metadata_small.json"

mkdir -p $OUTPUT_FOLDER

python3 filter.py $OUTPUT_METADATA $FILTERED_METADATA_JSON
python3 documents.py $FILTERED_METADATA_JSON $OUTPUT_FOLDER
python3 graph_facts.py $OUTPUT_FOLDER
python3 tf_idf.py $FILTERED_METADATA_JSON $OUTPUT_FOLDER $OUTPUT_STEMMED
python3 pagerank.py $FILTERED_METADATA_JSON $OUTPUT_FOLDER
python3 alias_data.py $FILTERED_METADATA_JSON $OUTPUT_FOLDER

mv $OUTPUT_FOLDER "static/"