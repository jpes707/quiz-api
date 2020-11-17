import pymongo
import keys

# keys.py example
#
# MONGO_USER = 'username'
# MONGO_PASSWORD = 'OHjGUJVRoE5puqZp'
# MONGO_ENDPOINT = 'questionscluster-nspyz.gcpa.mongodb.net'
# DB_NAME = 'QuestionsDatabase'
# COLLECTION_NAME = 'QuestionsCollection'

client = pymongo.MongoClient('mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE'.format(keys.MONGO_USER, keys.MONGO_PASSWORD, keys.MONGO_ENDPOINT, keys.DB_NAME))
questions_collection = client[keys.DB_NAME][keys.COLLECTION_NAME]
print(list(questions_collection.aggregate([{ '$sample': { 'size': 1 } }]))[0])
