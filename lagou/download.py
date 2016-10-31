import pymongo


def intoMongo(data):
    #检查数据库，去重后添加到数据库
    conn = pymongo.MongoClient(host='192.168.1.111', port=27017)
    db = conn['python']
    downloaded = db.lagou.find()
    if data not in downloaded:
        db.lagou.insert(data)