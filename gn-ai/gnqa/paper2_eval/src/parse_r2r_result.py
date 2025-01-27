import json
import sys
from document_operations import DocOps, QuestionList

verbose = 0
#read_file = '/home/shebes/Coding/gn-ai/gnqa/paper2_eval/data/testresp2.json'
read_file = '/home/shebes/Coding/gn-ai/gnqa/paper2_eval/data/responses/human/cs_diabetes_responses.json'
out_file = '../data/dataset/human/intermediate_files/human_cs_diabetes_' 

values_key = {
    "text" :           {"name": "contexts",      "append": 1},
    "associatedQuery": {"name": "question",      "append": 0},
    "id":              {"name": "id",            "append": 1},
    "title":           {"name": "titles",        "append": 1},
    "document_id":     {"name": "document_id",   "append": 1},
    "extraction_id":   {"name": "extraction_id", "append": 1},
    "content":         {"name": "answer",        "append": 0}
}

def get_ragas_out_dict():
    return { "titles":        [],
             "extraction_id": [],
             "document_id":   [],
             "id":            [],
             "contexts":      [],
             "answer":        "",
             "question":      ""}

def extract_response(obj, values_key, thedict):
    if isinstance(obj, dict):
        for key, val in obj.items():
            if (key in values_key.keys()):
                if (values_key[key]["append"]):
                    thedict[values_key[key]["name"]].append(val.replace("\n", " ").strip())
                else:
                    thedict[values_key[key]["name"]] = val.replace("\n", " ").strip()
                print(("", "Key -> {0}\tValue -> {1}".format(key,val)) [verbose])
            else:
                if (len(obj.items()) == 1 ):
                    print(key, " --> ", val)
            extract_response(val, values_key, thedict)
    elif isinstance(obj, list):
        for item in obj:
            extract_response(item, values_key, thedict)

# this should be a json file with a list of input files and an output file
with open(read_file, "r") as r_file:
    result_file = json.load(r_file)

ragas_output = {
    "titles":        [],
    "extraction_id": [],
    "document_id":   [],
    "id":            [],
    "contexts":      [],
    "answer":        "",
    "question":      ""}

print('There are {0} keys in the result file'.format(result_file.keys()))
for key in result_file.keys():
    eval_dataset_dict = get_ragas_out_dict()
    extract_response(result_file[key], values_key, eval_dataset_dict)
    DocOps.writeDatasetFile(eval_dataset_dict, '{0}{1}'.format(out_file, key))