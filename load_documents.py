import requests, json, os
from elasticsearch import Elasticsearch

directory = 'Documents/'

res = requests.get('http://localhost:9200')
print (res.content)

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}],timeout=60)

i = 1

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        f = open(directory+filename)
        docket_content = f.read()
        es.index(index='interview_experience', ignore=400, doc_type='docket', id=i, body=json.loads(docket_content))
        i = i + 1