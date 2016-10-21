from pymongo import MongoClient

#the document create mongo database of all the events that are given


def create_mongo_instance(DB_NAME, COLLECTION_NAME):
    client = MongoClient()
    db = client[DB_NAME]
    coll = db[COLLECTION_NAME]
    return db, coll

def store_data(table, timestamp, fraud_prob, name, json_string):
    table.insert_one({'timestamp':timestamp, 'fraud_prob':fraud_prob, 'name': name, 'data':json_string, })

def get_all_data(table):
    return list(table.find())

if __name__ == '__main__':
    db, table = create_mongo_instance("fraud", "fraud")
    store_data(table, '67890', "{'e':5, 'f':6}", 0.123456)
    print get_all_data()
