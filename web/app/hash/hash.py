
hash_data = [{ 'hid': 0, 'hname':'food'}, { 'hid': 1, 'hname':'sohwakhang'}]
item = [{'iid':0, 'iname':'abc', 'description':'provided by shinyongkim','req':10 }, {'iid':1, 'iname':'abc1', 'description':'provided by shinyongkim','req':10}, {'iid':2, 'iname':'abc2', 'description':'provided by shinyongkim','req':10}]
hash_map = [{'iid':0, 'hid':0}, {'iid':0, 'hid':1}]

follow_lst = [{'uid':0, 'iid':0}]

coll_hash_map.find({'iid':0}) # -> [{'iid':0, 'hid':0}, {'iid':0, 'hid':1}]
coll_hash_map.find({'hid':0}) # -> [{'iid':0, 'hid':0}]

import pymongo
conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database('flames')

col_user = db.get_collection('user')
col_hash_data = db.get_collection('hash_data')
col_item = db.get_collection('item')
col_follow = db.get_collection('follow')
col_hash_map = db.get_collection('hash_map')


col_user.delete_many({})
col_user.insert_many(user)

col_item.delete_many({})
col_item.insert_many(item)

def search(iid):
     col_item = db.get_collection('item')
     results = col_item.find({'iid':iid})
     return render_template() ##
