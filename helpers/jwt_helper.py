import jwt

def generateToken(userData, secretSignature, tokenLife): 
    try: 
        JWT_ALGORITHM = 'HS256'
        payload = {
            'user_id': userData,
        }
        jwt_token = jwt.encode(payload, secretSignature, JWT_ALGORITHM)
        return jwt_token
    except Exception as e:
        print(e)
        return e

def verifyToken(token, secretKey):
    try:
        JWT_ALGORITHM = 'HS256'
        payload = jwt.decode(jwt_token, 
            secretKey,
            algorithms=[JWT_ALGORITHM])
        return payload
    except:
        return 0