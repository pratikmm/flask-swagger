from flask import Flask, Blueprint, json
from flask_restplus import Api, Resource, fields
from functools import reduce
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

blueprint = Blueprint('api', __name__, url_prefix='/api')


authorizations = {
    'apikey' : {
        'type': 'apiKey',
        'in' : 'header',
        'name': 'Authorization'
    }
}

api = Api(blueprint, authorizations=authorizations, security='apikey', version='1.0', title='Sample API',
    description='A sample API', default="Records", default_label="record operations")#), doc='/documentation')#, doc=False

#loginapi = Api(blueprint, default="Authentication", default_label="Records")#), doc='/documentation')#, doc=False

app.register_blueprint(blueprint)

app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
app.config['SWAGGER_UI_JSONEDITOR'] = True
app.config.SWAGGER_UI_OPERATION_ID = True
app.config.SWAGGER_UI_REQUEST_DURATION = True




a_fname = api.model('fname', {'fname': fields.String('Enter first name')})
a_record = api.model('id', {'id': fields.Integer('Enter id of record')})
a_credentials = api.model('credentials', {'username': fields.String('Enter username'),
                                          'password': fields.String('Enter password')})

record_list = []
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
record_list = add_sample_data(record_list)

def add_record(fname):
    new_rec = dict()
    top_id = 0
    
    id_list = []
    for one_rec in record_list:
        id_list.append(one_rec['id'])
    f = lambda a,b: a if (a > b) else b
    top_id = reduce(f, id_list) + 1
    
    new_rec['id'] = top_id
    new_rec['fname'] = fname
    record_list.append(new_rec)
    
    return new_rec

def delete_record(id):
    deleted_rec = dict()
    for one_rec in record_list:
        if one_rec['id'] == id:
            deleted_rec = one_rec
            break
    if not deleted_rec == {}:
        print(deleted_rec)
        record_list.remove(deleted_rec)
        return deleted_rec
    else:
        return {id: 'record not found'}


@api.route('/records')
class Records(Resource):
    #@api.doc(security='apikey')
    @jwt_required
    def get(self):
        return record_list

    @jwt_required
    @api.expect(a_fname)
    def post(self):
        fname = api.payload['fname']
        if  id is None or not fname.isalpha():
            return {'input error': 'pass only aplhabets value for parameter fname'}, 401
        else:
            record = add_record(fname)
            return record, 201
    
    @jwt_required
    @api.expect(a_record)
    def delete(self):
        id = api.payload['id']
        if  id is None:
            return {'input error': 'pass integer value for parameter id'}, 401
        else:
            record = delete_record(int(id))
            return record, 201

@api.route('/login')
class Login(Resource):
    @api.doc(security=None)
    @api.expect(a_credentials)
    def post(self):
        username = api.payload['username']
        password = api.payload['password']
        if not username:
            return {"msg": "Missing username parameter"}, 400
        if not password:
            return {"msg": "Missing password parameter"}, 400
        if username != 'test' or password != 'test':
            ret = {'jwt': 'Bearer ' + create_jwt(identity=username)}
            return ret, 200

@api.route('/hello')
class Hello(Resource):
    @api.doc(security=None)
    def get(self):
        return {"Status":"Hello"}, 200


if __name__ == '__main__':
    #app.run()
    app.run(debug=True, host='0.0.0.0', port=80)