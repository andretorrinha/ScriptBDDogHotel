from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta

client = MongoClient("mongodb+srv://csmroot:H4fUhbar49gP5PAnvH9V@clusterteste.9310k.mongodb.net/casalsaomartinho?retryWrites=true&w=majority") #conexão ao cluster

db = client.casalsaomartinho  #base dados casalsaomartinho
col = db.reservations #colection reservations

#definir os diferentes tempo para criação da flag
del_time_cc = datetime.now() - timedelta(hours=3, minutes=0)
del_time_mb = datetime.now() - timedelta(hours=12, minutes=0)
del_time_pp = datetime.now() - timedelta(hours=1, minutes=0)
del_time_mbw = datetime.now() - timedelta(hours=1, minutes=0)

#testes
print("TOTAL DOCS:", col.count_documents({}))
print("CURRENT TIME:", del_time_cc)

#queries na colection
del_result_cc = col.delete_many({"createdAt": {"$gt": del_time_cc}, "payment":"cc"})
del_result_mb = col.delete_many({"createdAt": {"$gt": del_time_mb}, "payment":"mb"})
del_result_pp = col.delete_many({"createdAt": {"$gt": del_time_pp}, "payment":"pp"})
del_result_mbw = col.delete_many({"createdAt": {"$gt":del_time_mbw}, "payment":"mbw"})

#resultados
print ("delete count:", del_result_cc.deleted_count)
print ("delete count:", del_result_mb.deleted_count)
print ("delete count:", del_result_pp.deleted_count)
print ("delete count:", del_result_mbw.deleted_count)
