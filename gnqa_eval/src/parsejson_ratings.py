import json
import sys

"""
This file converts the json report from GNQA into a list of individual users
and their interactions with the system. At the moment we are getting their
questions, the systems answers, and their ratings of the overall system response.
Unfortunately the context is not saved with the answer.
"""
# report_data, ratings_dict
def reorg_json_report(obj, resp_lst, ratings):
  if isinstance(obj, dict):
    user_id = ''
    for key, val in obj.items():
      if (key == "user_id"):
        user_id = val
        if isKeyInList(resp_lst, val) == 0:
          resp_lst.append({val: ratings})
        else:
          print("\nKey {0} is already present".format(val))
      elif (key in ["query","answer","weight","task_id"]):
        ratings[key].append(val)
      #else:
      #  print('These are the current ratings --> {0}'.format(ratings))
    print('The ratings before being pushed to user_responses ->  {0}'.format(ratings))
    # add query to dictionary, if it is an update then don't update the ratings
    qcount = query_dict.setdefault(ratings["query"][0], 0)
    query_dict.update({ratings["query"][0]: qcount+1})
    update_ratings(resp_lst, user_id, ratings)
    if qcount == 0:
      taskquery_dict.setdefault(ratings["task_id"][0], ratings["query"][0])
      #update_ratings(resp_lst, user_id, ratings)
    #reorg_json_report(val, resp_lst, ratings)
  elif isinstance(obj, list):
    for item in obj:
      ratings = reset_ratings()
      reorg_json_report(item, resp_lst, ratings)



def create_resultset_from_file(resp_lst, file_name, output):
  with open(file_name, "r") as r_file:
    the_data = json.load(r_file)
  reorg_json_report(the_data, resp_lst, output)

def isKeyInList(the_lst, the_key):
  result = 0
  result_item = {}
  for the_item in the_lst:
    if the_key in the_item:
      result = 1
      result_item = the_item
  return result, result_item

def update_ratings(ratings, user_id, input_dict):
  key_ndx, ratings_dict = isKeyInList(ratings, user_id)
  if key_ndx == 0:
    ratings.append({user_id: input_dict})
  else:
    for key, val in input_dict.items():
      if isinstance(val,list):
        ratings_dict[user_id][key].append(val[0])
      else:
        ratings_dict[user_id][key].append(val)
      
def reset_ratings():
  return {
    "task_id": [],
    "weight": [],
    "answer": [],
    "query": []
  }

user_responses = []
ratings_out = {
  "task_id": [],
  "weight": [],
  "answer": [],
  "query": []
}

query_dict = {}
taskquery_dict = {}

try:
  read_file = str(sys.argv[1]) # e.g. doc_list.json
  outp_file = str(sys.argv[2])
except:
  exit('Example use "python3 parsejson_ratings.py data/ratings/2024_06_25-gnqa_responses.json data/ratings/[date]-out.json"')

#print('The input file is {0}, the output file is {1}'.format(read_file, outp_file))

create_resultset_from_file(user_responses, read_file, ratings_out)
print('The number of users is {0}'.format(len(user_responses)))
#print(json.dumps(ratings_out, indent=2))
with open(outp_file, "a") as the_data:
    the_data.write(",\n")
    the_data.write(json.dumps(user_responses, indent=2))

print("Greetings shabes!")
print('There are {0} unique queries.'.format(len(taskquery_dict)))
print(json.dumps(taskquery_dict, indent=2))
#get number of users
# get number of questions asked per user
# get average ratings

