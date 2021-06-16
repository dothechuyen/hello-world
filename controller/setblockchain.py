from os import error
import uuid
from bson.objectid import ObjectId

from flask.json import jsonify

import datetime

def setBagri(data,userid, mongo, handler):
    try: 
        user_collection = mongo.db.users
        result = user_collection.find_one({"_id" : ObjectId(userid)})
        if not result or result["role"] != '1': 
            return jsonify(status = 500, msg = "you are not admin")
        bagri_collection = mongo.db.bagris
        arr_product = []
        id = uuid.uuid1()
        time_end = ""
        if not "description" in data : 
            description = ""
        else :
            description = data["description"]
        result = handler.create_bagri(str(id), data["name"],data["time_start"], time_end,description, arr_product)
        print(result)
        bagri_collection.insert({
            "id" : str(id),
            "name": data["name"],
            "user_id" : ObjectId(userid)        
        })
        return jsonify(status = 200, msg= "thanh cong")

    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

def initProduct(product_id, userid, data, mongo, handler ):
    try: 
        group_collection = mongo.db.groups
        products_collection = mongo.db.products
        result = group_collection.find_one({"user_id" : ObjectId(userid)})
        if not result : 
            return jsonify(status =  500, msg =  "Bạn không phải là quản lý của group nào")
        Info = data["dataInfo"]
        genusid = uuid.uuid1()
        waterid = uuid.uuid1()
        soilid = uuid.uuid1()
        now = datetime.datetime.now()
        arr_action = []
        result1 = handler.create_product(product_id, Info[1], Info[3], Info[2], "", "0", str(now), [str(genusid)], [str(waterid)], [str(soilid)], arr_action,result["id_bagri"])
        print("product: " + result1)
        result2 = handler.get_bagri(result["id_bagri"])
        print(result2)
        arr_product = result2[5]
        arr_product.append(product_id)
        result3 = handler.create_bagri(result2[0], result2[1],result2[2], result2[3],result2[4], arr_product)
        print("bagri: " + result3)
        filter = { 'product_id': product_id }
        
        # Values to be updated.
        newvalues = { "$set": { 'address_contract': result1, 'genus_id' : str(genusid), 'water_id' : str(waterid),'soil_id' : str(soilid)}} 
        
        # Using update_one() method for single updation.
        products_collection.update_one(filter, newvalues) 
        return jsonify (status =  200)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

def setProduct(product_id, data, mongo, handler) :
    try: 
        product_collection = mongo.db.products
        now = datetime.datetime.now()
        
        temp = handler.get_product(product_id)
        result = handler.create_product(product_id, data[0], data[1], data[2],"", "0", temp[6], temp[7], temp[8], temp[9], temp[10], temp[11])
        print("setproduct: " + result)
        filter = { 'product_id': product_id }
        
        # Values to be updated.
        newvalues = { "$set": { 'data_info': data }} 
        product_collection.update_one(filter, newvalues) 
        return True
        
    except Exception as e: 
        print(e)
        return False

def setSoil(soid_id, data, product_id, handler) :
    try: 
        now = datetime.datetime.now()
        temp = handler.get_soil(soid_id)
        if temp[0] == "":
            result = handler.create_soil(soid_id, data[0], data[1], data[2], data[3],str(now), "", product_id)
            print("setsoil: " + result)
            return True
        else :
            result = handler.create_soil(soid_id, data[0], data[1], data[2], data[3],temp[5], str(now), product_id)
            print("setsoil: " + result)
            return True
    except Exception as e: 
        print(e)
        return False

def setWater(water_id, data, product_id, handler) :
    try: 
        now = datetime.datetime.now()
        temp = handler.get_water(water_id)
        if temp[0] == "":
            result = handler.create_water(water_id, data[0], data[1], data[2], data[3],str(now), "", product_id)
            print("setwater: " +result)
            return True
        else :
            result = handler.create_water(water_id, data[0], data[1], data[2], data[3],temp[5], str(now), product_id)
            print("setwater: " +result)
            return True
    except Exception as e: 
        print(e)
        return False

def setGenus(genus_id, data, product_id, handler) :
    try: 
        now = datetime.datetime.now()
        temp = handler.get_genus(genus_id)
        if temp[0] == "":
            result = handler.create_genus(genus_id, data[0], data[1], data[2],str(now), "", product_id)
            print("setgenus: " +result)
            return True
        else :
            result = handler.create_genus(genus_id, data[0], data[1], data[2],temp[4], str(now), product_id)
            print("setgenus: " +result)
            return True
    except Exception as e: 
        print(e)
        return False
def setaction(action_id, data, product_id, handler) : 
    try:
        arr_history = []
        action_name = data["name"]
        time = data["time"]
        description = data["description"]
        result = handler.create_action(action_id, action_name, time, description, product_id, arr_history)
        print("set action: "+result) 
        return True
    except Exception as e: 
        print(e)
        return False