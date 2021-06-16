from itertools import product
from logging import error
from re import A, DEBUG
from flask import request, jsonify
import json

import uuid
import datetime

import common.Constant as constant
from bson.objectid import ObjectId

import controller.setblockchain as setblc
import controller.getblockchain as getblc

def getListProduct(_userid, mongo):
    try: 
        user_collection = mongo.db.users
        product_collection = mongo.db.products
        househoulds_collection = mongo.db.contracts
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(_userid)})
        role = getInfodUserById["role"]

        items = []
        if(role == constant.Constants["LienGorup"]) :
            getContract = product_collection.find({"parent_id" :ObjectId(_userid)})
            for document in getContract: 
                temp = str(document["user_id"])
                document["user_id"] = temp
                temp = str(document["_id"])
                document["_id"] = temp
                temp = str(document["parent_id"])
                document["parent_id"] = temp
                items.append(document)
            return jsonify(status = 200, items = items)
        if(role == constant.Constants["Group"]):
            getContract = product_collection.find({"user_id" :ObjectId(_userid)})
            for document in getContract: 
                temp = str(document["user_id"])
                document["user_id"] = temp
                temp = str(document["_id"])
                document["_id"] = temp
                temp = str(document["parent_id"])
                document["parent_id"] = temp
                items.append(document)
            return jsonify(status = 200, items = items)
        if(role == constant.Constants["HouseHolds"]):
            getHouseHoldsByID = househoulds_collection.find({"user_id" :ObjectId(_userid)})
            for document in getHouseHoldsByID:
                getProduct = product_collection.find({"id": document["product_id"]})
                if getProduct :
                    items.append(getProduct)
            
            return jsonify(status = 200, items = items)
        return jsonify(status = 200, items = items)
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )

def getVietGap():   
    try: 
        return jsonify(status = 200, data = constant.Constants["VietGap"])
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )

def createProduct(data,userid, mongo, handler ):
    try: 
        group_collection = mongo.db.groups
        products_collection = mongo.db.products
        result = group_collection.find_one({"user_id" : ObjectId(userid)})
        if not result : 
            return jsonify(status =  500, msg =  "Bạn không phải là quản lý của group nào")
        id = uuid.uuid1()

        now = datetime.datetime.now()
        info_product = {
            "product_id" : str(id),
            "address_contract" : "",
            "name": data["dataInfo"][1],
            "user_id": ObjectId(userid),
            "parent_id": result["parent_id"],
            "data_info": data["dataInfo"],
            "status": False,
            "description": "",
            "genus_id" : "",
            "water_id" : "",
            "soil_id" : "", 
            "createAt" : now,
        }
        products_collection.insert(info_product)
        setblc.initProduct(str(id),userid, data, mongo, handler)
        temp = str(info_product["user_id"])
        info_product["user_id"] = temp
        temp = str(info_product["parent_id"])
        info_product["parent_id"] = temp
        temp = str(info_product["_id"])
        info_product["_id"] = temp
        return jsonify (status =  200, result = info_product )
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

def getProduct(tx_hash, userid, mongo, handler):
    try: 
        user_collection = mongo.db.users
        product_collection = mongo.db.products
        msg_collection = mongo.db.msg
        getInfodUserById =  user_collection.find_one({"_id" : ObjectId(userid)})
        getProduct = product_collection.find_one({"address_contract" : tx_hash})
        data_info = getProduct["data_info"]
        resultGetSoild = handler.get_soil(getProduct["soil_id"])
        resultGetWater = handler.get_water(getProduct["water_id"])
        resultGetGenus = handler.get_genus(getProduct["genus_id"])

        respInfo = {
            "name": "Thông tin mùa vụ",
            "data": [
            {
                "name": "Tên",
                "data": data_info[0],
            },
            {
                "name": "Địa điểm",
                "data": data_info[1],
            },
            {
                "name": "Diện tích",
                "data": data_info[2],
            },
            ],
        }
        respDat = {
            "name": "Thông tin về đất",
            "data": [
            {
                "name": "Loại đất",
                "data": resultGetSoild[1],
            },
            {
                "name": "Độ Ph",
                "data": resultGetSoild[2],
            },
            {
                "name": "Vị trí",
                "data": resultGetSoild[3],
            },
            {
                "name": "Miêu tả",
                "data": resultGetSoild[4],
            },
            ],
        }
        respNuoc = {
            "name": "Thông tin về nguồn nước",
            "data": [
            {
                "name": "Nguồn gốc",
                "data": resultGetWater[1],
            },
            {
                "name": "Độ Ph",
                "data": resultGetWater[2],
            },
            {
                "name": "Vị trí",
                "data": resultGetWater[3],
            },
            {
                "name": "Miêu tả",
                "data": resultGetWater[4],
            },
            ],
        }

        respGiong = {
            "name": "Thông tin về giống cây",
            "data": [
            {
                "name": "Tên giống",
                "data": resultGetGenus[1],
            },
            {
                "name": "Nguồn gốc",
                "data": resultGetGenus[2],
            },
            {
                "name": "Miêu tả",
                "data": resultGetGenus[3],
            },
            ],
        }

        respHistory = {
            "name": "Cấu hình ghi nhật kí",
            "data": [
            {
                "name": "Thời gian",
                "data": "",
            },
            {
                "name": "Hành động",
                "data": "",
            },
            {
                "name": "Miêu tả",
                "data": "",
            },
            ],
        }
        getMsg = msg_collection.find_one({ "address_contract": tx_hash })

        if not getMsg :
            status_msg = ""
        else :
            status_msg = getMsg["status"]
        return jsonify(
            status =  200,
            resp_info = respInfo,
            resp_dat = respDat,
            resp_giong = respGiong,
            resp_nuoc =  respNuoc,
            resp_history = respHistory,
            verify_contract = getProduct["status"],
            status_msg = status_msg,
        )
    except Exception as e: 
        return jsonify(status = 500, error = e)

def editProduct(data, auth, mongo,handler):
    try: 
        if (not "dataDat" in data) or (len(data["dataDat"]) != 4) :
            return jsonify( status= 500, msg= "Trường data dat null hoặc thiếu" )
        if (not "dataNuoc" in data) or (len(data["dataNuoc"]) != 4) :
            return jsonify( status= 500, msg= "Trường data nuoc null hoặc thiếu" )
        if (not "dataGiong" in data) or (len(data["dataGiong"]) != 3) :
            return jsonify( status= 500, msg= "Trường data giong null hoặc thiếu" )
        if (not "dataInfo" in data) or (len(data["dataInfo"]) != 3) :
            return jsonify( status= 500, msg= "Trường data giong null hoặc thiếu" )
        product_collection = mongo.db.products
        getProduct = product_collection.find_one({"address_contract" : data["address_contract"]})
        dataSoil = data["dataDat"]
        dataWater = data["dataNuoc"]
        dataGenus = data["dataGiong"]
        dataProduct = data["dataInfo"]
        if setblc.setSoil(getProduct["soil_id"] ,dataSoil, getProduct["product_id"], handler) == False: 
            return jsonify(status = 500 , msg = "fail soil")
        if setblc.setWater(getProduct["water_id"], dataWater, getProduct["product_id"], handler) == False: 
            return jsonify(status = 500 , msg = "fail soil")
        if setblc.setGenus(getProduct["genus_id"], dataGenus, getProduct["product_id"], handler) == False: 
            return jsonify(status = 500 , msg = "fail soil")
        if setblc.setProduct(getProduct["product_id"], dataProduct, mongo, handler) == False: 
            return jsonify(status = 500 , msg = "fail soil")
        return jsonify(  status =  200, msg =  "Ghi thông tin thành công" )
        
    except Exception as e: 
        return jsonify(status = 500, error = e)

def sendVerifyProduct(data, userid, mongo):
    try: 
        msg_collection = mongo.db.msg
        product_collection = mongo.db.products

        tx_hash = data["address_contract"]
        reqType = data["type"]
        
        checkExistType = msg_collection.find_one({"address_contract" : tx_hash, "type" : reqType})

        if checkExistType and checkExistType["status"] != "3" :
            return jsonify(status = 200, msg = "The request has been accepted")

        getProduct = product_collection.find_one({"address_contract" : tx_hash, "user_id" : ObjectId(userid)})
        now = datetime.datetime.now()
        data = {
            "user_id": ObjectId(userid),
            "user_id_lien_group": getProduct["parent_id"],
            "product_id" : getProduct["_id"],
            "type" : str(reqType),
            "address_contract" : tx_hash,
            "status" : 1, 
            "updateAt" : now
        }
        msg_collection.insert(data)
        return jsonify(status = 200)
    except Exception as e: 
        return jsonify(status = 500, error = e)

def setVerifyProduct(data, userid, mongo):
    try: 
        msg_collection = mongo.db.msg
        product_collection = mongo.db.products
        user_collection = mongo.db.users

        msgId = data["msg_id"]

        getInfodUserById = user_collection.find_one({"_id" : ObjectId(userid)})
        if getInfodUserById["role"] != "1":
            return jsonify(status = 500, msg = "you are not admin list group" )

        result = msg_collection.find_one({"_id" : ObjectId(msgId)})
        
        filter = { '_id': result["product_id"]}
        # Values to be updated.
        newvalues = { "$set": { "status" : True, }} 
        
        # Using update_one() method for single updation.
        product_collection.update_one(filter, newvalues)

        now = datetime.datetime.now()
        filter1 = { '_id': ObjectId(msgId) }
        # Values to be updated.
        newvalues1 = { "$set": { "status" : 2, "updateAt" : now}} 
        
        # Using update_one() method for single updation.
        msg_collection.update_one(filter1, newvalues1) 
        
        return jsonify(status = 200, msg = "Accepted")
    except Exception as e: 
        return jsonify(status = 500, error = e)

def getListMsg(userid, mongo):
    try: 
        user_collection = mongo.db.users
        msg_collection = mongo.db.msg

        getInfodUserById = user_collection.find_one({"_id" : ObjectId(userid)})
        if getInfodUserById["role"] != "1" :
            return jsonify(status = 500, msg = "You are not admin list group")

        items = []        
        getAllMsg = msg_collection.find({"user_id_lien_group" : ObjectId(userid)})

        for document in getAllMsg: 
            get_user = user_collection.find_one({"_id" : document["user_id"]})
            document["user_id"] = get_user["email"]
            temp = str(document["_id"])
            document["_id"] = temp
            temp = str(document["user_id_lien_group"])
            document["user_id_lien_group"] = temp
            temp = str(document["product_id"])
            document["product_id"] = temp
            items.append(document)
        print(items)   
        return jsonify(status = 200, items = items)
    except Exception as e: 
        return jsonify(status = 500, error = e) 

def rejectVerify(data, mongo):
    try: 
        msg_collection = mongo.db.msg

        msgId = data["msg_id"]

        now = datetime.datetime.now()
        filter1 = { '_id': ObjectId(msgId) }
        # Values to be updated.
        newvalues1 = { "$set": { "status" : 3, "updateAt" : now}} 
        
        # Using update_one() method for single updation.
        msg_collection.update_one(filter1, newvalues1)
        
        return jsonify(status = 200, msg = "Rejected")
        
    except Exception as e: 
        return jsonify(status = 500, error = e)

def getListAction(tx_hash, userId, mongo, handler):
    try: 
        user_colleciton = mongo.db.users
        product_collection = mongo.db.products
        
        getInfodUserById = user_colleciton.find_one({"_id" : ObjectId(userId)})
        getProduct = product_collection.find_one({"address_contract" : tx_hash})

        role = getInfodUserById["role"]

        if role != "2":
            return jsonify(status = 500, msg= "You are not admin group")
        
        if not getProduct : 
            return jsonify(status = 500, msg = "product is not empty")
        
        arr_action = getblc.getListAction(str(getProduct["product_id"]), handler)
        items = []
        if len(arr_action) == 0: 
            return jsonify(status = 200, items = items)
    except Exception as e: 
        return jsonify(status = 500, error = e)  

def setaction( data, userid, mongo, handler):
    try:
        action_name = data["action_name"]
        description = data["description"]
        address_contract = data["address_contract"]
        user_collection = mongo.db.users
        product_collection = mongo.db.products
        household_collection = mongo.db.households
        contract_collection = mongo.db.contracts
        msgaction_collection = mongo.db.msg_actions
        
        getContractByAddressContract = contract_collection.find_one({"address_contract": address_contract})
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(userid)})
        role = getInfodUserById["role"]
        getProduct = product_collection.find_one({"address_contract" : address_contract})
        
        product_id = getProduct["product_id"]
        id = uuid.uuid1()
        if (role != constant.Constant["Group"]):
            return jsonify(status = 500, msg=" Ban khong cos quyen tao action!")
        getAllHousehold = household_collection.find({"parent_group_id": userid, "contract_id": getContractByAddressContract["_id"]})
        for i in range(0, len(getAllHousehold)):
            data_insert={
                "user_id": userid,
                "user_id_household": getAllHousehold[i]["user_id"],
                "status":0,
                "address_contract": address_contract,
                "data": ""
            }
            msgaction_collection.insert(data_insert)
        set_action = setblc.setaction(str(id), data, product_id, handler)
        return jsonify(status=200, msg="Tao Action thanh cong")
    except Exception as e: 
        return jsonify(status = 500, error = e) 

def setStatusMsgAaction(data, mongo):
    try:
        msgActionId = data["msg_action_id"]
        status = data["status"]
        datas = data["data"]
        
        user_collection = mongo.db.users
        product_collection = mongo.db.products
        household_collection = mongo.db.households
        contract_collection = mongo.db.contracts
        msgaction_collection = mongo.db.msg_actions
        
        #getInfodUserById = user_collection.find_one({"_id" : ObjectId(userid)})
        if datas:
            msgaction_collection.update_one({"_id": msgActionId},
                                            {"$set": {"status": status, "data": datas}})
        else:
            update = msgaction_collection.update_one({"_id": msgActionId},
                                            {"$set": {"status": status}})
        return jsonify(status = 200, msg = "update thanh cong")
    except Exception as e: 
        return jsonify(status = 500, error = e)   
    
def getMsgActionForFarmer(tx_hash, userid, mongo, handler):
    try:
        address_contract = tx_hash
        msgaction_collection = mongo.db.msg_actions
        user_collection = mongo.db.users
        
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(userid)})
        get_msg_action = msgaction_collection.find({"user_id_household": userid,
                                                    "address_contract": address_contract})
        return jsonify(status= 200, items = get_msg_action)
    except Exception as e: 
        return jsonify(status = 500, error = e) 

def change(data, userid, mongo, handler) :
    try:
        msgId = data["msg_id"]
        status = data["status"]
        
        user_collection = mongo.db.users
        msg_collection = mongo.db.msg
        
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(userid)})
        role = getInfodUserById["role"]
        
        if role != constant.Constant["LienGroup"]:
            return jsonify(status = 500, msg="Bạn không có quyền , chỉ liên nhóm mới có thể get msg")
        updateContract = msg_collection.update_one({"_id":msgId}, 
                                                   {"$set": {"status": status}})
        return jsonify(status=200, msg="update thanh cong!")
    except Exception as e: 
        return jsonify(status = 500, error = e) 