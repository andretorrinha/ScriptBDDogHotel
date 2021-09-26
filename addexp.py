import logging
import pytz
import os
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
from pymongo import MongoClient

###
#configurar logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#####
#Ler variavel conection_string do .env
load_dotenv()
MONGO_CONECTION_STRING = os.getenv('DBURL')

#####
#conexão base de dados
client = MongoClient(MONGO_CONECTION_STRING) #conexão ao cluster
db = client.casalsaomartinho  #base dados casalsaomartinho
col = db.reservations #colection reservations

#####
#loop para realizar o update na variavel exp_flag de todos os metodos de pagamento

def checkpagamentos():
    #definir os diferentes tempos para ativaçao da flag, 
    current_time = datetime.now(pytz.utc) + timedelta(hours=1, minutes=0) #UTC JA É MENOS UMA HORA LOGO 2 = 3
    #####
    #criação de listas com a informação dos metodos de pagamento, e dos tempos de remoção
    payment_methods = ["cc", "mb", "mbw"]
    try:
        for value in range(len(payment_methods)):
            update_result_cc = col.update_many(
                {"payment":payment_methods[value], "status":0},
                { "$set": {"exp_time":current_time + timedelta(hours = 12)}}
            )
        logging.info("Criado um exp data")

    except Exception as e:
        logging.exception("Erro a criar exp data", exc_info=True)

checkpagamentos()

#####
#Encerrar a conexão com a bd
client.close()
