from logging import error
import flask 
from flask import request, jsonify
from flask_pymongo import PyMongo
from werkzeug.datastructures import auth_property
from werkzeug.wrappers import response


import controller.product as product
import controller.user as user
import controller.setblockchain as setblc

# some_file.py
import sys
# # insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'D:\\GR1\\bagri_sdk')

#import py_handler
from bagri_sdk.py_handler import Handler as handler

#handler = Handler()

 

import re

import middlewares.AuthMiddleware as middleWare
 
# Make a regular expression
# for validating an Email
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


app = flask.Flask(__name__)
#app.config["DEBUG"] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/bgri"
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/v0/signup', methods=['POST'])
def register():    
    data = request.get_json() 
    print(data)   
    if (not "email" in data) or (not re.search(regex, data["email"])) :
        return jsonify(status = 500, 
        msg = "Please enter a valid email" )    
    if not "password" in data :
        return jsonify(status = 500, 
        msg = "Please enter a valid password." )
    if not "role" in data :
        return jsonify(status = 500, 
        msg = "Please enter a valid role." )
    if not "name" in data :
        name = ""
    else :
        name = data["name"]
    email = data ["email"]
    password = data["password"]
    role = data["role"]
    return user.sign_up(name, email, password, role, mongo)

@app.route('/v0/login', methods=['POST'])
def login():
    data = request.get_json()   
    if (not "email" in data) or (not re.search(regex, data["email"])) :
        return jsonify(status = 500, 
        msg = "Please enter a valid email" )    
    if not "password" in data :
        return jsonify(status = 500, 
        msg = "Please enter a valid password." )
    email = data ["email"]
    password = data["password"]
    return user.login(email, password, mongo)

#quan ly lien nhom: role = 1
#in ra danh sach cac nhom
@app.route('/v0/get_list_group', methods=['POST'])
def get_list_group():
    try : 
        data = request.get_json()
        print(data)
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return user.getListGroup(data, auth, mongo)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
#them nhom moi
@app.route('/v0/add_groups', methods=['POST'])
def add_groups():
    data = request.get_json()
    print(data)
    if (not "email" in data) or (not re.search(regex, data["email"])) :
        return jsonify(status = 500, 
        msg = "Please enter a valid email" )
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return user.addGroup(data, auth, mongo)
        # print(auth)
        # return jsonify(status = 500, 
        #     msg = "Please enter a valid password." )
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
#tao mua vu moi
@app.route('/v0/create_bgri', methods=['POST'])
def create_bgri():  
    data = request.get_json()
    print(data)
    if (not "time_start" in data) or (not "name" in data):
        return jsonify(status = 500, 
        msg = "Please enter a valid time start or name" )
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return setblc.setBagri(data, auth, mongo, handler)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
    # return jsonify(success = True,
    #     message = "thanh cong",
    #     id_bagri= str(id) )

@app.route('/v0/get_list_bgri', methods=['GET'])
def get_list_bgri():
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return user.getListBgri(auth, mongo)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )

#------------------------------------------------------------------

#quan ly nhom : role = 2 
@app.route('/v0/add_households', methods=['POST'])
def add_households():
    data = request.get_json()
    if (not "email" in data) or (not re.search(regex, data["email"])) :
        return jsonify(status = 500, 
        msg = "Please enter a valid email" )
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return user.addHouseHold(data, auth, mongo)
        # print(auth)
        # return jsonify(status = 500, 
        #     msg = "Please enter a valid password." )
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
# quan ly lien nhom, quan ly nhom, ho dan : role = 1, 2, 3
@app.route('/v0/get_list_product', methods=['GET'])
def getListProduct():
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.getListProduct(auth, mongo)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )

@app.route('/v0/get_tieu_chuan_vietgap', methods=['GET'])
def getVietGap():
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.getVietGap()
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )

@app.route('/v0/deploy_contracts_vietgap', methods=['POST'])
def create_product():
    try: 
        data = request.get_json()
        print(data)
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.createProduct(data, auth, mongo, handler)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )

@app.route('/v0/<id>/<contract_id>/get_list_households', methods=['GET'])
def getListHouseHolds(id, contract_id):
    try: 
        print(id + "---" + contract_id)
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return user.getListHouseHolds(id, contract_id,mongo)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )     

@app.route('/v0/<address_contract>/get_product', methods=['GET'])
def getProduct(address_contract):
    if not address_contract: 
        return jsonify(status = 500, msg= "tx hash is not empty" )
    try: 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.getProduct(address_contract, auth,mongo, handler)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )     

@app.route('/v0/write_product', methods=['POST'])
def editProduct():
    try:
        data = request.get_json()
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.editProduct(data, auth, mongo, handler)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

@app.route('/v0/send_yeu_cau_verify', methods=['POST'])
def verifyProduct():
    try:
        data = request.get_json()
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.sendVerifyProduct(data, auth, mongo)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

@app.route('/v0/set_verify_contract', methods=['POST'])
def setVerifyProduct():
    try:
        data = request.get_json()
        print(data)
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.setVerifyProduct(data, auth, mongo)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

@app.route('/v0/get_list_msg', methods=['GET'])
def getListMsg():
    try:
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.getListMsg(auth, mongo)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

@app.route('/v0/reject', methods=['POST'])
def rejectVerify():
    try:
        data = request.get_json()
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.rejectVerify(data, mongo)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

@app.route('/v0/<address_contract>/get_qr_code', methods=['GET'])
def getListAction(address_contract):
    if not address_contract: 
        return jsonify(status = 500, msg= "tx hash is not empty" )
    try: 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.getListAction(address_contract, auth,mongo, handler)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e ) 

@app.route('/v0/set_qr_code', methods = ['POST'])
def setaction():
    try:
        data = request.get_json()
        print(data)
        if (not "action_name" in data) or (not re.search(regex, data["action_name"])) :
            return jsonify(status = 500, 
            msg = "Action_name khong ton tai!" )
        if (not "description" in data) or (not re.search(regex, data["description"])) :
            return jsonify(status = 500, 
            msg = "description khong ton tai!" )
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.setaction(data, auth, mongo, handler)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
        
@app.route('/v0/set_status_msg_action', methods = ['POST'])
def setsttmsg():
    try:
        data = request.get_json()
        if (not "msg_action_id" in data) or (not re.search(regex, data["msg_action_id"])) :
            return jsonify(status = 500, 
            msg = "msg_action_id khong ton tai!" )
        if (not "status" in data) or (not re.search(regex, data["status"])) :
            return jsonify(status = 500, 
            msg = "status khong ton tai!" )
        return product.setStatusMsgAaction(data, mongo)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
        
@app.route('/v0/<address_contract>/get_msg_action_for_farmer', methods=['GET'])
def getmsgaction4farm(address_contract):
    if not address_contract: 
        return jsonify(status = 500, msg= "tx hash is not empty" )
    try: 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.getMsgActionForFarmer(address_contract, auth,mongo, handler)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e ) 
        
@app.route('/v0/change', methods = ['POST'])
def change():
    try:
        data = request.get_json()
        if (not "msg_id" in data) or (not re.search(regex, data["msg_id"])) :
            return jsonify(status = 500, 
            msg = "msg_id khong ton tai!" )
        if (not "status" in data) or (not re.search(regex, data["status"])) :
            return jsonify(status = 500, 
            msg = "status khong ton tai!" )
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.change(data, auth, mongo, handler)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
app.run()