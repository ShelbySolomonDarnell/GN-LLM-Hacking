import os
import sys
import json
import configparser
import pandas as pd

from pandas import DataFrame as df
from langchain_together import Together
from langchain_together.embeddings import TogetherEmbeddings
from ragas.metrics import (faithfulness, answer_relevancy, context_relevancy, context_recall, context_utilization, context_precision)
from ragas import evaluate
from datasets import Dataset#, load_dataset

config = configparser.ConfigParser()
config.read('_config.cfg')

os.environ["OPENAI_API_KEY"] = config['key.api']['openai']
together_key = config['key.api']['togetherai']

#embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-8k-retrieval")
embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-32k-retrieval")

together_completion = Together(
    #model="NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT",
    #model="togethercomputer/Llama-2-7B-32K-Instruct",
    #model="meta-llama/Llama-3-70b-chat-hf",
    model="google/gemma-7b-it",
    temperature=0.8,
    max_tokens=4000,
    top_k=1,
    together_api_key=together_key
)

read_file = str(sys.argv[1])
outp_file = str(sys.argv[2])

print(read_file)
print(outp_file)

with open(read_file, "r") as r_file:
    data = json.load(r_file)

dataset = Dataset.from_dict(data)
print(dataset)

"""
results = evaluate(
    dataset,
    metrics=[faithfulness,answer_relevancy,context_relevancy,context_utilization],
    llm=together_completion,
    embeddings=embeddings)
"""
results = evaluate(dataset,
                   metrics=[faithfulness,answer_relevancy,context_relevancy,context_utilization])

print(results)

with open(outp_file, "a") as the_data:
    the_data.write(",\n")
    the_data.write(json.dumps(results, indent=2))

#df_results = results.to_pandas()
#df_results.head()
