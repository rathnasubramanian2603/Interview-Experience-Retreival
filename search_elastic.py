from flask import Flask,Response, render_template,request
from elasticsearch import Elasticsearch
app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}],timeout=60)
@app.route('/')
def start():
   return render_template('query.html')

columns = [
  {
    "field": "company", # which is the field's name of data key
    "title": "company_name", # display as the table header's name
    "sortable": True,
  },
  {
    "field": "title",
    "title": "Title",
    "sortable": True,
  },
  {
    "field": "url",
    "title": "URL",
    "sortable": True,
  },
]

@app.route('/query',methods = ['POST', 'GET'])
def hello_world():
   if request.method == 'GET':
      query = request.args.get('query')
      company = request.args.get('company')
      output = es.search(index='interview_experience', body={'query': {
       'bool':{
      'should': [
        {'match': {'content':  query}},
        {'match': {'company': company}}
      ]
    }
    }
    }
    )
      out=[]
      for i in output['hits']['hits']:
         jsonData = {"title": "", "company": "", "content": "", "url":""}
         jsonData['title']=i['_source']['title']
         jsonData['company'] = i['_source']['company']
         jsonData['url']=i['_source']['url']
         out.append(jsonData)
      return render_template("table.html",data=out,columns=columns,title='Interview Experience')


if __name__ == '__main__':
   app.debug = True
   app.run()
   app.run(debug=True)
