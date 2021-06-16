from bson.objectid import ObjectId
import jwt
import common.Constant as constant

def isAuth(request, mongo):
    jwt_token = request.headers.get('x-access-token')
    if jwt_token:
        JWT_ALGORITHM = 'HS256'
        try:
            payload = jwt.decode(jwt_token, 
                constant.Constants["ACCESS_TOKEN_SECRET"],
                algorithms=[JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return {"msg" : 'Token is invalid.', "status":403}
        id = payload['user_id']
        user_collection = mongo.db.users
        result = user_collection.find_one({"_id": ObjectId(id)})
        if result :
            return id
        else :
            return {"msg" : 'Token is invalid.', "status":401}
    else : 
        return {"msg" : 'No token provided.', "status":403}