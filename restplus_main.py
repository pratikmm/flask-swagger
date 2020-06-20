from flask import Flask, send_from_directory, jsonify, request, Blueprint
from flask_restplus import Api, Resource, fields
from flask_api import status
import os
import json
from functools import reduce
from werkzeug.utils import cached_property


app = Flask(__name__)
api = Api(app)
#blueprint = Blueprint('api', __name__, url_prefix='/api')
#api = Api(blueprint, doc='/documentation')#,doc=False
#app.register_blueprint(blueprint)

#app.config['SWAGGER_UI_JSONEDITOR'] = True

db_list = []
def add_sample_data(op_list):
    id = []
    fname = []
    id = [1, 2, 3]
    fname = ['ram', 'shyam', 'naam']
    # op_list = []
    for i in range(0, len(id)):
        temp_dict = dict()
        temp_dict['id'] = id[i]
        temp_dict['fname'] = fname[i]
        op_list.append(temp_dict)
    return op_list
db_list = add_sample_data(db_list)

def get_record(id):
    response_rec = dict()
    for one_rec in db_list:
        if one_rec['id'] == id:
            response_rec = one_rec
            break
    if not response_rec == {}:
        return response_rec
    else:
        return {id: 'record not found'}

def add_record(fname):
    new_rec = dict()
    top_id = 0
    
    id_list = []
    for one_rec in db_list:
        id_list.append(one_rec['id'])
    f = lambda a,b: a if (a > b) else b
    top_id = reduce(f, id_list) + 1
    
    new_rec['id'] = top_id
    new_rec['fname'] = fname
    db_list.append(new_rec)
    
    return new_rec

def delete_record(id):
    deleted_rec = dict()
    for one_rec in db_list:
        if one_rec['id'] == id:
            deleted_rec = one_rec
            break
    if not delete_record == {}:
        print(deleted_rec)
        db_list.remove(deleted_rec)
        return deleted_rec
    else:
        return {id: 'record not found'}
    

@app.route('/getallrecords',methods = ['GET'])
def getallrecords():
    return jsonify(db_list), status.HTTP_200_OK

@app.route('/getrecord',methods = ['GET'])
def getrecord():
    print(request)
    id = request.args.get('id')
    if  id is None or not id.isnumeric():
        return jsonify({'input error': 'pass integer value for parameter id'}), status.HTTP_400_BAD_REQUEST
    else:
        record = get_record(int(id))
        return jsonify(record), status.HTTP_200_OK

@app.route('/addrecord',methods = ['PUT'])
def addrecord():
    print(request)
    fname = request.args.get('fname')
    if  id is None or not fname.isalpha():
        return jsonify({'input error': 'pass only aplhabets value for parameter fname'}), status.HTTP_400_BAD_REQUEST
    else:
        record = add_record(fname)
        return jsonify(record), status.HTTP_200_OK

@app.route('/deleterecord',methods = ['DELETE'])
def deleterecord():
    print(request)
    id = request.args.get('id')
    if  id is None or not id.isnumeric():
        return jsonify({'input error': 'pass integer value for parameter id'}), status.HTTP_400_BAD_REQUEST
    else:
        record = delete_record(int(id))
        return jsonify(record), status.HTTP_200_OK






if __name__ == '__main__':
    
    app.run()