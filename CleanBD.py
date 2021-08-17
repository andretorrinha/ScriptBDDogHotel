from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta

#conexão base de dados
client = MongoClient("mongodb+srv://csmroot:H4fUhbar49gP5PAnvH9V@clusterteste.9310k.mongodb.net/casalsaomartinho?retryWrites=true&w=majority") #conexão ao cluster
db = client.casalsaomartinho  #base dados casalsaomartinho
col = db.reservations #colection reservations

#####

#definir os diferentes tempo para criação da flag
del_time_cc = datetime.now() - timedelta(hours=3, minutes=0)
del_time_mb = datetime.now() - timedelta(hours=12, minutes=0)
del_time_mbw = datetime.now() - timedelta(hours=1, minutes=0)
del_time_pp = datetime.now() - timedelta(hours=1, minutes=0)

#####

#criação de listas com a informação dos metodos de pagamento, e dos tempos de remoção
payment_del_time = [del_time_cc, del_time_mb, del_time_mbw, del_time_pp]
payment_methods = ["cc", "mb", "mbw", "pp"]

#####

#loop para realizar o update na variavel exp_flag de todos os metodos de pagamento
for value in range(4):
    update_result_cc = col.update_many(
        {"createdAt": {"$gt": payment_del_time[value]}, "payment":payment_methods[value], "status":0},
        { "$set": {"exp_flag":1}}
    )
    print("Found count:", update_result_cc.matched_count)
    print("Updated count:", update_result_cc.modified_count)


