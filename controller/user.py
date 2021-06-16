from typing import ItemsView
from flask import request, jsonify
import json
import helpers.jwt_helper as jwtHelper
import common.Constant as constant
from bson.objectid import ObjectId


def sign_up( _name, _email, _password, _role, mongo):
    user_collection = mongo.db.users
    checkEmail = user_collection.find_one({"email": _email })
    if checkEmail : 
        print("false")
        return jsonify(status = 500, 
            msg = "Email already exists ")
    user_collection.insert({
        "name": _name,
        "email": _email,
        "password": _password,
        "role": str(_role),
        "address": "0xe4680B5B373b9353AF87De622a6E410E067a25c9",
        "private_key":
          "ef0be3ad9cf6ab09b1aaca99e1880546e4ca82e159a590291d0ec67e5929d0cf",
      })
    print("true")
    return jsonify(status = 200,
        message = "thanh cong" )

def login(_email, _password, mongo):
    try:
        user_collection = mongo.db.users
        result = user_collection.find_one({"email": _email, "password": _password })
        if result :    
            temp = str(result["_id"])
            result["_id"] = temp
            accessToken = jwtHelper.generateToken(result["_id"],
                constant.Constants["ACCESS_TOKEN_SECRET"],
                constant.Constants["ACCESS_TOKEN_LIFE_RESET_PASSWORD"])
            return jsonify(status = 200, 
                msg = "thanh cong",
                user = result ,
                access_token =  accessToken)
        else: 
            return jsonify(status = 500, 
                msg = "login fail")
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )

def getListGroup(data, _userid, mongo):
    try:
        user_collection = mongo.db.users
        group_collection = mongo.db.groups
        id_bagri = data["id_bgri"]
        items = []
        result = group_collection.find({"parent_id" : ObjectId(_userid), "id_bagri" : id_bagri})
        if not result :
            return jsonify(status = 500,
                items = items)
        for document in result: 
            getInfoUser = user_collection.find_one({"_id" : document["user_id"]})
            getInfoUser["name"] = document["name_group"]
            temp = str(getInfoUser["_id"])
            getInfoUser["_id"] = temp
            items.append(getInfoUser)
        return jsonify(status = 200, items = items)
        
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )
        
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )

def addGroup(data, _userid,mongo):
    try:
        user_collection = mongo.db.users
        group_collection = mongo.db.groups
        getUserById = user_collection.find_one({"email": data["email"]})
        if not getUserById or getUserById["role"] != '2': 
            return jsonify(status = 500, 
                msg = "email not found or is not intergroup")
        checkExistGroups =  group_collection.find_one({"user_id" : getUserById["_id"]})
        if checkExistGroups : 
            return jsonify(status = 500, 
                msg = "Email already exists in the group")
        data = {
            "user_id" : getUserById["_id"],
            "parent_id" : ObjectId(_userid),
            "id_bagri" : data["id_bgri"],
            "name_group" : data["name"]
        }
        result = group_collection.insert(data)
        temp = str(result)
        return jsonify(status = 200, 
            result = temp)
        
    except Exception as e:
        return jsonify(status = 500, 
                error = e )

def getListBgri(_userid, mongo):
    try:
        bagri_collection = mongo.db.bagris
        items = []
        result = bagri_collection.find({"user_id" : ObjectId(_userid)})
        if not result :
            return jsonify(status = 500,
                items = items)
        for document in result: 
            temp = {
                "name" : document["name"],
                "id" : document["id"]
            }
            items.append(temp)
        return jsonify(status = 200, items = items)
        
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )

def addHouseHold(data, userid, mongo):
    try:
        user_collection = mongo.db.users
        product_collection = mongo.db.products
        households_collection = mongo.db.households
        email = data["email"]
        product_id = data["contract_id"]
        getUserById = user_collection.find_one({"_id" : ObjectId(userid)})
        if (getUserById["role"] != "2"):
            return jsonify(status = 500, msg = "you need permission")
        getProductByUserId = product_collection.find_one({"_id" : ObjectId(product_id)})
        if not getProductByUserId : 
            return jsonify(status = 500, msg = "can't find product")
        getUserByEmail = user_collection.find_one({"email" : email})
        if (not getUserByEmail ) or (getUserByEmail["role"] != '3') :
            return jsonify(status = 500, 
                msg = "Cant find email or email is not households")
        checkExitsGroups = households_collection.find_one({"user_id": getUserByEmail["_id"], "product_id": ObjectId(product_id)})
        if checkExitsGroups : 
            return jsonify(status = 500, msg = "Email already exists in the household")
        data = {
            "user_id" : getUserByEmail["_id"],
            "parent_group_id" : ObjectId(userid),
            "product_id" : ObjectId(product_id)
        }
        households_collection.insert(data)
        
        return jsonify(status = 200, 
            result = 0)
        
    except Exception as e:
        return jsonify(status = 500, 
                error = e )

def getListHouseHolds(useid, _idproduct, mongo):
    try: 
        households_collection = mongo.db.households
        user_collection = mongo.db.users
        result = households_collection.find({"product_id" : ObjectId(_idproduct), "parent_group_id" : ObjectId(useid)})
        items = []
        if not result : 
            return jsonify(status = 200, items = items)
        for document in result:
            getInfoUser = user_collection.find_one({"_id" : document["user_id"]})
            temp = str(getInfoUser["_id"])
            getInfoUser["_id"] = temp
            items.append(getInfoUser)
        return jsonify(status = 200, items = items)
    except Exception as e: 
        return jsonify(status = 500, msg = e)