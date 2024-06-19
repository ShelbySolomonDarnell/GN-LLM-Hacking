import json
import sys


def iterate_json(obj, thedict):
    if isinstance(obj, dict):
        for key, val in obj.items():
            if (key == "text"):
                thedict["contexts"].append(val.replace("\n", " ").strip())
            elif (key == "answer"):
                thedict["answer"] = val.replace("\n", " ").strip()
            elif (key == "question"):
                thedict["question"] = val.replace("\n", " ").strip()
            else:
                if (len(obj.items()) == 1 ):
                    print(key, " --> ", val)
            iterate_json(val, thedict)
    elif isinstance(obj, list):
        for item in obj:
            iterate_json(item, thedict)

def create_dataset_from_files(tag, file_name, rag_out):
    for the_file in file_name[tag]:
        ragas_output = {
            "contexts": [],
            "answer": "",
            "question": ""}
        #print(the_file)
        with open("./data/"+the_file, "r") as r_file:
            data_file = json.load(r_file)
        iterate_json(data_file, ragas_output)
        rag_out["answer"].append(ragas_output["answer"])
        rag_out["question"].append(ragas_output["question"])
        rag_out["contexts"].append(ragas_output["contexts"])

def create_resultset_from_file(file_name):
        with open("./data/"+the_file, "r") as r_file:
            data_file = json.load(r_file)
        iterate_json(data_file, ragas_output)


file_list_tag = str(sys.argv[1])
read_file = str(sys.argv[2]) # e.g. doc_list.json
outp_file = str(sys.argv[3])

rag_out = {
    "question": [],
    "answer": [],
    "contexts": []
}

cntxt_lst = []

# this should be a json file with a list of input files and an output file
with open(read_file, "r") as r_file:
    file_lst = json.load(r_file)

create_dataset_from_files(file_list_tag, file_lst, rag_out)

with open(outp_file, "a") as the_data:
    #json.dump(ragas_output, the_data)
    the_data.write(",\n")
    the_data.write(json.dumps(rag_out, indent=2))
