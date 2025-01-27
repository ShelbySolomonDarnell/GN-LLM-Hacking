import json
import sys
import os

from r2r import R2RClient
from document_operations import DocOps, QuestionList

'''
*******************************************************************************
Variables
*******************************************************************************
'''
rag_response = {}
client       = R2RClient("http://localhost:8000")
health_resp  = client.health()

'''
*******************************************************************************
Commands
*******************************************************************************
'''

print("The R2R client's health status is {0}".format(health_resp))

try:
    read_file = str(sys.argv[1])
    out_file  = str(sys.argv[2])
except:
    exit('Example use "python run_questions.py ../data/questions/human/de/aging.json ../data/responses/human/de/aging_resp.json"')

qLst = QuestionList(read_file, 1) # second parameter is for verbose output
ndx = 1
for question in qLst.get("domainexpert","aging"):
    print('Getting response for the following question --> {0}'.format(question))
    rag_response[str(ndx)] = client.rag(question)
    ndx += 1

DocOps.writeDatasetFile(rag_response, out_file)