import os
import sys
import json
import time
import configparser
import apis.process as gnqa
from apis.process import get_gnqa, get_response_from_taskid


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
        combo_text = item['comboTxt']
        combo_text = combo_text.replace('\n','')
        combo_text = combo_text.replace('\t','')
        result.append(combo_text)
    return result

def writeDatasetFile(responses, outp_file):
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
        print(query)
        task_id, answer, refs = get_gnqa(query, config['key.api']['fahamuai'], config['DEFAULT']['DATA_DIR'])
        responses['question'].append(query)
        responses['answer'].append(answer)
        responses['task_id'].append(task_id)
        responses['contexts'].append(simplifyContext(refs))
        ndx+=1
        time.sleep(10) # sleep a bit to not overtask the api
        if ndx % 5 == 0:
          print('Will print to file number {0}'.format(int(ndx/5)))
          outp_file  = '{0}dataset_{1}_{2}_{3}.json'.format(config['out.response.dataset']['gpt4o_dir'],level,domain,str(int(ndx/5)))
          writeDatasetFile(responses, outp_file)
          responses = reset_responses()
    if len(responses['question']) > 0:
        #print('Will print to file number {0}'.format(int((ndx/5)+1)))
        #print(responses)
        outp_file  = '{0}dataset_{1}_{2}_{3}.json'.format(config['out.response.dataset']['gpt4o_dir'],level,domain,str(int(ndx/5)+1))
        writeDatasetFile(responses, outp_file)

def parse_responses(jsonfile):
    data_lst = {
       "general": {
          "user_id": [],
          "query": [],
          "answer": [],
          "task_id": [],
          "level": ""
       },
       "aging": {
          "user_id": [],
          "query": [],
          "answer": [],
          "task_id": [],
          "level": ""
       },
       "diabetes": {
          "user_id": [],
          "query": [],
          "answer": [],
          "task_id": [],
          "level": ""
       }
    }
    for item in jsonfile:
        domain = ''
        for key, val in item.items():
           user_id = key
           resp_data = val
           ndx = 0
           for task_id in resp_data["task_id"]:
              thequery = resp_data["query"][ndx]


           # loop through lists, adding data to appropriate key in data_lst
           #domain = key
        level     = "human"
        #item[]
        query_lst = item[domain]["query"]
        task_lst  = item[domain]["task_id"]
        answers   = item[domain]["answer"]
        create_datasets_from_taskid(task_lst, query_lst, answers, domain, level)

def create_datasets_from_taskid(task_list, query_list, answers, domain, level):
    responses = reset_responses()
    ndx = 0
    for task_id in task_list:
        _, _, refs = get_response_from_taskid(config['key.api']['fahamuai'], task_id)
        responses['question'].append(query_list[ndx])
        responses['answer'].append(answers[ndx])
        responses['task_id'].append(task_id)
        responses['contexts'].append(simplifyContext(refs))
        ndx+=1
        time.sleep(10) # sleep a bit to not overtask the api
        if ndx % 5 == 0:
          #print('Will print to file number {0}'.format(int(ndx/5)))
          outp_file  = '{0}dataset_{1}_{2}_{3}.json'.format(config['out.response.dataset']['human_dir'],level,domain,str(int(ndx/5)))
          writeDatasetFile(responses, outp_file)
          responses = reset_responses()
    if len(responses['question']) > 0:
        #print('Will print to file number {0}'.format(int((ndx/5)+1)))
        #print(responses)
        outp_file  = '{0}dataset_{1}_{2}_{3}.json'.format(config['out.response.dataset']['human_dir'],level,domain,str(int(ndx/5)+1))
        writeDatasetFile(responses, outp_file)

#print(json.dumps(query_responses, indent=2))

# read json file
# get level domain and query for output file
responses = {
    'question': [],
    'answer':   [],
    'contexts':  [],
    'task_id': []
}

try: 

  read_file = str(sys.argv[1])
  file_type = str(sys.argv[2])

except:
  exit('Example use "python3 retrieve_context.py data/queries/qlist.json human/gpt4o"')



with open(read_file, "r") as r_file:
  file_lst = json.load(r_file)
if file_type == "gpt4o":
  parse_document(file_lst)
else:
  parse_responses(file_lst)