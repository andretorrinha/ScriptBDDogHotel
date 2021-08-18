from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_CONECTION_STRING = os.getenv('MONGO_CONECTION_STRING')

#conexão base de dados
client = MongoClient(MONGO_CONECTION_STRING) #conexão ao cluster
db = client.casalsaomartinho  #base dados casalsaomartinho
col = db.reservations #colection reservations

#####
#definir os diferentes tempos para ativaçao da flag, 
#CUIDADO COM POTENCIAIS DIFERENÇAS EM HORAS COM O DEEPLOY NO SERVER
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
for value in range(len(payment_methods)):
    update_result_cc = col.update_many(
        {"createdAt": {"$lt": payment_del_time[value]}, "payment":payment_methods[value], "status":0},
        { "$set": {"exp_flag":1}}
    )
    print("Found ", payment_methods[value], " count:", update_result_cc.matched_count)
    print("Updated ", payment_methods[value], " count:", update_result_cc.modified_count)

#####
#Encerrar a conexão com a bd
client.close()
