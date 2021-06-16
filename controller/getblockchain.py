from os import error

def getGenos(idGenos, handler) :
    try: 
        result = handler.get_genus(idGenos)
        print(result)
        return result
    except Exception as e: 
        return e

def getWater(idWater, handler) :
    try: 
        result = handler.get_water(idWater)
        return result
    except Exception as e: 
        return e

def getSoid(idSoid, handler) :
    try: 
        result = handler.get_soid(idSoid)
        return result
    except Exception as e: 
        return e       

def getListAction(idProduct, handler):
    try: 
        result = handler.get_product(idProduct)
        return result[10]
    except Exception as e: 
        return e 