import os
import sys
import json
import time
import configparser
import apis.process as gnqa
from apis.process import get_gnqa, get_response_from_taskid


config = configparser.ConfigParser()
config.read('_config.cfg')

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

def parse_document(jsonfile):
  print('Parse document')
  for item in jsonfile:
    level     = item['level']
    domain    = item['domain']
    query_lst = item['query']
    create_datasets(query_lst, domain, level)

def create_datasets(query_list, domain, level):
  print('Creating dataset')
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
      outp_file  = '{0}dataset_{1}_{2}_{3}.json'.format(config['out.response.dataset']['human_dir'],level,domain,str(int(ndx/5)))
      writeDatasetFile(responses, outp_file)
      responses = reset_responses()
  if len(responses['question']) > 0:
    outp_file  = '{0}dataset_{1}_{2}_{3}.json'.format(config['out.response.dataset']['human_dir'],level,domain,str(int(ndx/5)+1))
    writeDatasetFile(responses, outp_file)

def parse_responses(jsonfile):
  print('Parsing human responses')
  de_dict_general  = {"level": "domainexpert",     "domain": "general",  "query": [], "task_id": []}
  de_dict_aging    = {"level": "domainexpert",     "domain": "aging",    "query": [], "task_id": []}
  de_dict_diabetes = {"level": "domainexpert",     "domain": "diabetes", "query": [], "task_id": []}
  cs_dict_general  = {"level": "citizenscientist", "domain": "general",  "query": [], "task_id": []}
  cs_dict_aging    = {"level": "citizenscientist", "domain": "aging",    "query": [], "task_id": []}
  cs_dict_diabetes = {"level": "citizenscientist", "domain": "diabetes", "query": [], "task_id": []}
  j = 0
  for _, val in jsonfile.items():
    ndx = 0
    lvl = val.get("level")
    for qry in val.get("query"):
      ans = val.get("answer")[ndx] if "answer" in val else ""
      tpc  = val.get("topic")[ndx]
      tpc = "general" if tpc==0 else "aging" if tpc==1 else "diabetes"
      tskd = val.get("task_id")[ndx]
      if   lvl == 'cs' and tpc == 'general':
        addToDataList(cs_dict_general, qry, ans, tskd)
      elif lvl == 'cs' and tpc == 'aging':
        addToDataList(cs_dict_aging, qry, ans, tskd)
      elif lvl == 'cs' and tpc == 'diabetes':
        addToDataList(cs_dict_diabetes, qry, ans, tskd)
      elif lvl == 'de' and tpc == 'general':
        addToDataList(de_dict_general, qry, ans, tskd)
      elif lvl == 'de' and tpc == 'aging':
        addToDataList(de_dict_aging, qry, ans, tskd)
      elif lvl == 'de' and tpc == 'diabetes':
        addToDataList(de_dict_diabetes, qry, ans, tskd)
      else:
         print('Somehow there is a query without a topic or expertise level')
      ndx+=1
    j+=1
  create_datasets_from_taskid(de_dict_general)
  create_datasets_from_taskid(de_dict_aging)
  create_datasets_from_taskid(de_dict_diabetes)
  create_datasets_from_taskid(cs_dict_general)
  create_datasets_from_taskid(cs_dict_aging)
  create_datasets_from_taskid(cs_dict_diabetes)

def addToDataList(data_lst, qry, ans, tskd):
  data_lst["query"].append(qry)
  data_lst["task_id"].append(tskd)
  if "answer" not in data_lst.keys():
    data_lst["answer"] = []
  data_lst["answer"].append(ans)


def create_datasets_from_taskid(info_dict):#task_list, query_list, answers, domain, level):
  print('Creating dataset of questions from {0} in the topic of {1}'.format(info_dict["level"], info_dict["domain"]))
  responses = reset_responses()
  ndx = 0
  query_list = info_dict["query"]
  if "answer" in info_dict:
    answers    = info_dict["answer"]
  else:
    info_dict["answer"] = []
    answers = []

  for task_id in info_dict["task_id"]:
    _, an_answer, refs = get_response_from_taskid(config['key.api']['fahamuai'], task_id)
    responses['question'].append(query_list[ndx])
    if answers[ndx] == "":
      responses['answer'].append(an_answer)
    else:
      responses['answer'].append(answers[ndx])
    responses['task_id'].append(task_id)
    responses['contexts'].append(simplifyContext(refs))
    ndx+=1
    time.sleep(10) # sleep a bit to not overtask the api
    if ndx % 5 == 0:
      #print('Will print to file number {0}'.format(int(ndx/5)))
      outp_file  = '{0}dataset_{1}_{2}_{3}_two.json'.format(config['out.response.dataset']['human_dir'],info_dict["level"],info_dict["domain"],str(int(ndx/5)))
      writeDatasetFile(responses, outp_file)
      responses = reset_responses()
  if len(responses['question']) > 0:
    #print('Will print to file number {0}'.format(int((ndx/5)+1)))
    #print(responses)
    outp_file  = '{0}dataset_{1}_{2}_{3}_two.json'.format(config['out.response.dataset']['human_dir'],info_dict["level"],info_dict["domain"],str(int(ndx/5)+1))
    writeDatasetFile(responses, outp_file)

try: 

  read_file = str(sys.argv[1])
  file_type = str(sys.argv[2])

except:
  exit('Example use "python3 retrieve_context.py data/queries/qlist.json human/gpt4o"')


print('Read input file')
with open(read_file, "r") as r_file:
  file_lst = json.load(r_file)
if file_type == "gpt4o":
  parse_document(file_lst)
else:
  parse_responses(file_lst)