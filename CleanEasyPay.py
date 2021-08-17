from pymongo import MongoClient
import urllib.request
import json

#conexão base de dados
client = MongoClient("mongodb+srv://csmroot:H4fUhbar49gP5PAnvH9V@clusterteste.9310k.mongodb.net/casalsaomartinho?retryWrites=true&w=majority") #conexão ao cluster
db = client.casalsaomartinho  #base dados casalsaomartinho
col = db.reservations #colection reservations




body = {'ids': [12, 14, 50]}
myurl = "http://www.testmycode.com"

req = urllib.request.Request(myurl)
req.add_header('Content-Type', 'application/json; charset=utf-8')
jsondata = json.dumps(body)
jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
req.add_header('Content-Length', len(jsondataasbytes))
response = urllib.request.urlopen(req, jsondataasbytes)


#Encerrar a conexão com a bd
client.close()