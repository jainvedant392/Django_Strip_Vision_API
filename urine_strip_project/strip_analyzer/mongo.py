from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['urine_strip_db']
collection = db['strip results']
