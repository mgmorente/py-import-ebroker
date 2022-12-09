import json
import os
import psycopg2
from config import config
from utils import *
import shutil


setting = config(section='setting')
path_files = setting["path_files"]

recibos_estado = []
polizas_ramos = []
polizas_cias = []


#########################################################

prCyan('>> Importar Polizas')
polizasList = importFile('polizas')

# with open(f'{os.path.dirname(__file__)}/exportacion/polizas-ramo-vacio.csv', 'w+') as f:
#     for r in polizasList: 
#         if int(get_ramo_pacc(r["producto"])) == 0: 
#             f.write(f'{r["producto"]};{r["cod_poliza_cia"]}\n')
# f.close()    

#########################################################

for r in polizasList: 
    if int(get_ramo_pacc(r["producto"])) == 0: 
        polizas_ramos.append(r["producto"])
    if int(getCodCia(r["cia_poliza"])) == 0: 
        polizas_cias.append(r["cia_poliza"])
    
if list(dict.fromkeys(polizas_ramos)) != []: 
    print('Ramos sin equivalencia: ',list(dict.fromkeys(polizas_ramos)))

if list(dict.fromkeys(polizas_cias)) != []: 
    print('Cias sin equivalencia: ',list(dict.fromkeys(polizas_cias)))


#########################################################

# prCyan('>> Importar Recibos')
# recibosList = importFile('recibos')

# for r in recibosList: 
#     recibos_estado.append(r["estado"])

# if list(dict.fromkeys(recibos_estado)) != []: 
#     print(list(dict.fromkeys(recibos_estado)))

#########################################################    



# Mensaje fin proceso
prGreen('Success!')
