from flask import Flask, jsonify, request, make_response
import pandas as pd
import json
from Handler import Handler
from DataParsing import dataparsing
app = Flask(__name__)

@app.route('/api/query', methods=['GET','POST'])
def login():
    val = request.args.get('fuzzy')
    input_query = request.get_json()
    if not input_query:
        return jsonify({'msg': 'Missing JSON'}),400
    handler = Handler()
    #print(input_query['input_query'])
    if(handler.query(input_query['input_query'],val))==False:
        return jsonify({'msg': 'Query Syntax error'}),400
    if val == 'True':
        return handler.query(input_query['input_query'],True)
    else:
        return handler.query(input_query['input_query'],False)
'''
df = pd.DataFrame({'video_id':['difhiwhefiuwh','difhiwhefiuwh','difhiwhefiuwh','difhiwhefiuwh','difhiwhefiuwh'],
                   'video_url':['siuhdiuhf','siuhdiuhf','siuhdiuhf','siuhdiuhf','siuhdiuhf'],
                   'video_location':['eifiwehfih','siuhdiuhf','siuhdiuhf','siuhdiuhf','siuhdiuhf'],
                   'start_frame':[12,12,12,12,12],
                   'end_frame':[1212,1212,1212,1212,1212]})

@app.route('/api/data', methods=['GET','POST'])
def fetchDetails():
    result = {}
    for index, row in df.iterrows():
        result[index] = dict(row)
    p = DataParser()
    #if normal_query():
    return make_response(jsonify(p.query()),200)
    #else:
        #return make_response(jsonify(p.fuzzyQuery()),200)
'''
if __name__ == '__main__':
    app.run(debug=True)