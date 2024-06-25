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
    #qcount = query_dict.setdefault(ratings["query"][0], 0)
    #query_dict.update({ratings["query"][0]: qcount+1})
    #if qcount == 0:
    update_ratings(resp_lst, user_id, ratings)
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

def add_ratings_value(ratings, user_id, key, val):
  _, ratings_dict = isKeyInList(ratings, user_id)
  ratings_dict[user_id][key].append(val)
    
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

"""
ratings_out["task_id"] = ["2D8205C79915FF9CEB8DECCE51E6E473"]
ratings_out["weight"] = [1]
ratings_out["answer"] = ["1. Study by Kaeberlein (2013b) on the use of Rapamycin in preventing organ transplant rejection, some forms of cancer, and restenosis in cardiac stents.\n2. Study by Mannick et al. (2014) on the use of Rapamycin derivative RAD001 in improving age-associated decline in immune function in elderly people.\n3. Study by Yi et al. (2014) on the use of Rapamycin in improving outcomes in a glycogen storage disease model.\n4. Study by Paoloni et al. (2010) on the use of Rapamycin in veterinary clinical trials for osteosarcoma.\\n5. Study by Kaeberlein (2015) on the use of Rapamycin in assessing side effects and effects on age-associated cardiac function in elderly dogs.\n6. Study by Meric-Bernstam and Gonzalez-Angulo (2009) on the use of Rapamycin in the context of cancer.\n7. Study by Larson et al. (2016) on the use of Rapamycin in determining initial dosing regimens in healthy dogs.\n8. Study by Dai et al. (2014) and Flynn et al. (2013) on the use of Rapamycin in improving cardiac function in laboratory mice.\n9. Study by Johnson et al. (2015) on the use of Rapamycin in improving health and reducing mortality in middle-aged companion dogs.\n10. Study by Chen et al. (2009) on the use of Rapamycin in delaying aging in mice.\n11. Study by Augustine et al. (2007) and de Oliveira et al. (2011) on the side effects of Rapamycin.\n12. Study by Lamming et al. (2012) on the possible side effects of Rapamycin on glucose homeostasis.\n13. Study on the use of Rapamycin as a CRM due to its modulating properties over proteostasis.\n14. Study by Johnson et al. (2013) on the use of Rapamycin in extending lifespan and delaying age-related functional declines in rodents."]
ratings_out["query"] = ["List as  many studies as you can that include  rapamycin."]

user_id_1 = "b4601142-3b57-4d5b-9b55-80bdf0ea4599"
user_responses.append({user_id_1: ratings_out})

ratings_out = {}
ratings_out["task_id"] = ["849E78D8214245F8E8167E78C01BEE60"]
ratings_out["weight"] = [1]
ratings_out["answer"] = ["The varying efficacy of diabetes treatments among individuals can be attributed to genetic variants present in drug receptors or drug metabolizers, such as OCT genes, KCNJ11, ABCC8, and CYP2C9. These genetic variants can influence the metabolism, transportation, and therapeutic mechanisms of antidiabetic drugs, leading to differences in drug disposition, glycemic response, tolerability, and incidence of adverse effects. Additionally, gene-gene, gene-environment, and gene-treatment interactions may also contribute to the variation in disease progression and response to therapy."]
ratings_out["query"] = ["What are the genetic bases for the varying efficacy of diabetes treatments among individuals?"]


user_id_2 = "e031ac19-fec1-4d97-a037-cd39d3817c54"
user_responses.append({user_id_2: ratings_out})
#print(json.dumps(user_responses,indent=2))

task_id = ""
weight  = 0
answer  = ""

#add_ratings_value(user_responses, user_id_2, "weight", weight)
#print(json.dumps(user_responses,indent=2))

"""

read_file = str(sys.argv[1]) # e.g. doc_list.json
outp_file = str(sys.argv[2])

#print('The input file is {0}, the output file is {1}'.format(read_file, outp_file))

create_resultset_from_file(user_responses, read_file, ratings_out)
print('The number of users is {0}'.format(len(user_responses)))
#print(json.dumps(ratings_out, indent=2))
with open(outp_file, "a") as the_data:
    the_data.write(",\n")
    the_data.write(json.dumps(user_responses, indent=2))

print("Greetings shabes!")

#get number of users
# get number of questions asked per user
# get average ratings

