import xml.etree.ElementTree as ET
import psycopg2

from config import config
from utils import prCyan, prRed

######### bd
# conn = psycopg2.connect(database="ctm",
#                         host="localhost",
#                         user="postgres",
#                         password="postgres",
#                         port="5432")

# read database configuration
params = config()
# connect to the PostgreSQL database
conn = psycopg2.connect(**params)

polizasBdList = []

cur = conn.cursor()
cur.execute("select cia_poliza, nif, poliza from polizas where compania = 49")

for table in cur.fetchall(): 
    polizasBdList.append(table)

conn.commit()
cur.close()


######### xml                        
tree = ET.parse('fiatc-cartera.xml')
root = tree.getroot()

# xmlList = []
contador = 0

for poliza in root.findall("Objetos/Poliza"):
    
    idPoliza = poliza.find('DatosPoliza/IdPoliza')
    ramo = poliza.find('DatosPoliza/DatosRamo/RamoEntidad')
    nif = poliza.find('Tomador/PersonaFisica/IdPersona')

    if nif is None:
        nif = poliza.find('Tomador/PersonaJuridica/IdPersona')
    
    for poliza in polizasBdList:
        # comparar nif
        if poliza[1] == nif.text:
            # comparar 2 primeros digitos y ultimos 4 digitos de la poliza
            if poliza[0][-4:] == idPoliza.text[-4:] and poliza[0][0:2] == idPoliza.text[0:2]:
                nRamo = ramo.text.ljust(2,'0')
                nPoliza = str(idPoliza.text).zfill(7)
                # print(poliza[0],  nRamo + nPoliza)
                print(f"UPDATE polizas SET cia_poliza = '{nRamo + nPoliza}' WHERE poliza = '{poliza[2]}';")
                contador += 1
    
    # xmlList.append( (idPoliza.text, ramo.text, nif.text) )

prCyan(f'>> {contador} registros')


