import logging
import pytz
import os
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
###
#configurar logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#####
#Ler variavel conection_string do .env
load_dotenv()
MONGO_CONECTION_STRING = os.getenv('MONGO_CONECTION_STRING')

#####
#conexão base de dados
client = MongoClient(MONGO_CONECTION_STRING) #conexão ao cluster
db = client.casalsaomartinho  #base dados casalsaomartinho
col = db.reservations #colection reservations

#####
#loop para realizar o update na variavel exp_flag de todos os metodos de pagamento

@sched.scheduled_job('interval', hours=1)
def checkpagamentos():
    #definir os diferentes tempos para ativaçao da flag, 
    del_time_cc = datetime.now(pytz.utc) - timedelta(hours=2, minutes=0) #UTC JA É MENOS UMA HORA LOGO 2 = 3
    del_time_mb = datetime.now(pytz.utc) - timedelta(hours=11, minutes=0) # 12H
    del_time_mbw = datetime.now(pytz.utc) - timedelta(hours=1, minutes=0) # 2H
    del_time_pp = datetime.now(pytz.utc) - timedelta(hours=1, minutes=0) # 2H
    #####
    #criação de listas com a informação dos metodos de pagamento, e dos tempos de remoção
    payment_del_time = [del_time_cc, del_time_mb, del_time_mbw, del_time_pp]
    payment_methods = ["cc", "mb", "mbw", "pp"]
    try:
        for value in range(len(payment_methods)):
            update_result_cc = col.update_many(
                {"createdAt": {"$lt": payment_del_time[value]}, "payment":payment_methods[value], "status":0},
                { "$set": {"status":9}}
            )
            print("Found ", payment_methods[value], " count:", update_result_cc.matched_count)
            print("Updated ", payment_methods[value], " count:", update_result_cc.modified_count)
        logging.info("Os valores sobre o estado de pagamento levaram update")
        
    except Exception as e:
        logging.exception("Erro a dar update na bd", exc_info=True)

sched.start()

#####
#Encerrar a conexão com a bd
client.close()
