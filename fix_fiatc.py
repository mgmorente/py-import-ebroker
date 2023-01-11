import xml.etree.ElementTree as ET
import psycopg2

######### bd
conn = psycopg2.connect(database="ctm",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432")

polizasBdList = []

cur = conn.cursor()
cur.execute("select cia_poliza, nif from polizas where compania = 49")

for table in cur.fetchall(): 
    polizasBdList.append(table)

conn.commit()
cur.close()


######### xml                        
tree = ET.parse('fiatc-cartera.xml')
root = tree.getroot()

xmlList = []
contador = 0

for poliza in root.findall("Objetos/Poliza"):
    
    idPoliza = poliza.find('DatosPoliza/IdPoliza')
    ramo = poliza.find('DatosPoliza/DatosRamo/RamoEntidad')
    nif = poliza.find('Tomador/PersonaFisica/IdPersona')

    if nif is None:
        nif = poliza.find('Tomador/PersonaJuridica/IdPersona')
    
    xmlList.append( (idPoliza.text, ramo.text, nif.text) )

    contador += 1

print(' -- Numero registros', contador, '--')


