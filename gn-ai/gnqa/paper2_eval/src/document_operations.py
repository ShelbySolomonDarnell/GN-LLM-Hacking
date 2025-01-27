import os
#import sys
import json
#import time
#import configparser
'''
from r2r import ( R2R, 
                  Document, 
                  GenerationConfig, 
                  R2RClient )
'''

class DocOps:
    _type = ''
    values_key = {
        "text" :           {"name": "contexts",      "append": 1},
        "associatedQuery": {"name": "question",      "append": 0},
        "id":              {"name": "id",            "append": 1},
        "title":           {"name": "titles",        "append": 1},
        "document_id":     {"name": "document_id",   "append": 1},
        "extraction_id":   {"name": "extraction_id", "append": 1},
        "content":         {"name": "answer",        "append": 0}
    }

    def __init__(self):
        self._type = 'QuestionList'

    def reset_responses():
        return {
            'question': [],
            'answer':   [],
            'contexts':  []
            #,
            #'task_id': []
        }

    def writeDatasetFile(responses, outp_file):
        print(outp_file)
        output = json.dumps(responses, indent=2)
        if os.path.exists(outp_file):
            with open(outp_file, "a") as the_data:
                the_data.write('\n\n' + output)
        else:
            with open(outp_file, "a") as the_data:
                the_data.write(output)

    def get_r2r_ragas_out_dict():
        return { "titles":        [],
                "extraction_id": [],
                "document_id":   [],
                "id":            [],
                "contexts":      [],
                "answer":        "",
                "question":      ""}

    def read_json_document(file_name):
        with open(file_name, "r") as result_file:
            return json.load(result_file)
    
    def combine_responses(doc_lst, out_filename):
        ragas_output = DocOps.reset_responses()

        for doc in doc_lst:
            the_doc = DocOps.read_json_document(doc)
            ragas_output['question'].append(
                the_doc['question'])
            ragas_output['answer'].append(
                the_doc['answer'])
            ragas_output['contexts'].append(
                the_doc['contexts'])
        DocOps.writeDatasetFile(
            ragas_output, out_filename)


    def extract_response(obj, values_key, thedict):
        if isinstance(obj, dict):
            for key, val in obj.items():
                if (key in values_key.keys()):
                    if (values_key[key]["append"]):
                        thedict[values_key[key]["name"]].append(val.replace("\n", " ").strip())
                    else:
                        thedict[values_key[key]["name"]] = val.replace("\n", " ").strip()
                    print(("", "Key -> {0}\tValue -> {1}".format(key,val)) [DocOps.verbose])
                else:
                    if (len(obj.items()) == 1 ):
                        print(key, " --> ", val)
                DocOps.extract_response(val, values_key, thedict)
        elif isinstance(obj, list):
            for item in obj:
                DocOps.extract_response(item, values_key, thedict)

class QuestionList:
    _verbose = 0
    _doc = ''
    _fname = ''
    _question_list = {
        "domainexpert": { 
            "gn":  [],
            "aging":    [],
            "diabetes": []
        },
        "citizenscientist": { 
            "gn":  [],
            "aging":    [],
            "diabetes": []
        }
    }

    def __init__(self, the_file, verbose=0):
        print('QuestionList has been initialized {0}, verbosity is {1}'.format(the_file, verbose))
        self._fname = the_file
        self._verbose = verbose
        self.read_document()
        self.parse_document()
        #self._print()


    def read_document(self):
        self._doc = DocOps.read_json_document(
            self._fname)



    def parse_document(self):
        print(('', '\nParse question list') [self._verbose] )
        for item in self._doc:
            level     = item['level']
            domain    = item['domain']
            query_lst = item['query']
            self._question_list[level][domain] = query_lst
            #print(('', 'Level --> {0} \tDomain --> {1}\n{2}'.format(level, domain, self.print_list(query_lst))) [self._verbose])
            #create_datasets(query_lst, domain, level)


    def print_list(self, the_lst):
        ndx = 1 
        for item in the_lst:
            print('\t[{0}] {1}'.format(ndx, item))
            ndx += 1
    
    def _print(self):
        print(json.dumps(self._question_list, indent=2))

    def get(self, level, domain):
        return self._question_list[level][domain]
    

