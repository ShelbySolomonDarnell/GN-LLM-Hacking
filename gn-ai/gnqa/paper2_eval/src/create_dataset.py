#!/usr/bin/python3

import sys
from document_operations import DocOps


'''
*******************************************************************************
Commands
*******************************************************************************
'''

try:
    read_file = str(sys.argv[1])
    out_file  = str(sys.argv[2])
except:
    exit('Example use "python create_dataset.py ../data/lists/human_list_cs_gn.json ../data/dataset/human_cs_gn.json"')

doc_list = DocOps.read_json_document(read_file)
DocOps.combine_responses(doc_list, out_file)