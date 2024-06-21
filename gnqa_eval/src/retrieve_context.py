import os
import sys
import json
import time
import configparser
import apis.process as gnqa
from apis.process import get_gnqa


config = configparser.ConfigParser()
config.read('_config.cfg')

print('The fahamu api key is --> {0}'.format(config['key.api']['fahamuai']) )

'''
the refs object is a list of items containing doc_id, bibInfo, and comboTxt
We only need comboTxt
'''
def simplifyContext(refs):
    result = []
    for item in refs:
        result.append(item["comboTxt"])
    return result

def writeDatasetFile(responses, level, domain, ndx):
    outp_file  = '{0}dataset_{1}_{2}_{3}.json'.format(config['out.response.dataset']['gpt4o_dir'],level,domain,str(int(ndx)))
    print(outp_file)
    #print(json.dumps(responses,indent=2))
    output = json.dumps(responses, indent=2)
    if os.path.exists(outp_file):
        with open(outp_file, "a") as the_data:
            the_data.write('' + output)
    else:
        with open(outp_file, "a") as the_data:
            the_data.write(output)


def reset_responses():
    return {
        'question': [],
        'answer':   [],
        'contexts':  [],
        'task_id': []
    }
'''
You need a function to take a file and read a question or a list of questions and 
write the full responses to disk. Place the responses in different files
as long as its (mod%5+2) documents.
'''

def parse_document(jsonfile):
    for item in jsonfile:
        level     = item['level']
        domain    = item['domain']
        query_lst = item['query']
        create_datasets(query_lst, domain, level)


def create_datasets(query_list, domain, level):
    responses = reset_responses()
    ndx = 0
    for query in query_list:

        task_id, answer, refs = get_gnqa(query, 
                                         config['key.api']['fahamuai'], 
                                         config['DEFAULT']['DATA_DIR'])
        responses['question'].append(query)
        responses['answer'].append(answer)
        responses['task_id'].append(task_id)
        responses['contexts'].append(simplifyContext(refs))
        ndx+=1
        time.sleep(5) # sleep a bit to not overtask the api
        if ndx % 5 == 0:
            print('Will print to file number {0}'.format(int(ndx/5)))
            writeDatasetFile(responses, level, domain, int(ndx/5))
            responses = reset_responses()
    if len(responses['question']) > 1:
        print('Will print to file number {0}'.format(int((ndx/5)+1)))
        print(responses)
        #writeDatasetFile(responses, level, domain, (ndx/5)+1)


#print(json.dumps(query_responses, indent=2))

# read json file
# get level domain and query for output file
responses = {
    'question': [],
    'answer':   [],
    'contexts':  [],
    'task_id': []
}

read_file = str(sys.argv[1])
with open(read_file, "r") as r_file:
    file_lst = json.load(r_file)

parse_document(file_lst)

