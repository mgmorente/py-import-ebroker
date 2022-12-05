import json
import os
import psycopg2
from config import config
from utils import *
import shutil




recibos_estado = []
polizas_ramos = []

#########################################################

prCyan('>> Importar Polizas')
polizasList = importFile('polizas')

for r in polizasList: 
    if int(get_ramo_pacc(r["producto"])) == 0: 
        polizas_ramos.append(r["producto"])

if list(dict.fromkeys(polizas_ramos)) != []: 
    print(list(dict.fromkeys(polizas_ramos)))

#########################################################

prCyan('>> Importar Recibos')
recibosList = importFile('recibos')

for r in recibosList: 
    recibos_estado.append(r["estado"])

if list(dict.fromkeys(recibos_estado)) != []: 
    print(list(dict.fromkeys(recibos_estado)))

#########################################################    



# Mensaje fin proceso
prGreen('Success!')
