import json
import psycopg2
from config import config
from utils import *

# Fn borrar datos y tablas
def borrar_datos():
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE tag = 'INI'")
    cur.execute("DELETE FROM polizas WHERE tag = 'INI'")
    cur.execute("DELETE FROM relacion_codigo_cliente_nif")
    conn.commit()
    cur.close()

# Fn ver datos por pantalla
def ver_datos(r):
    print(
        r["cod_cliente"],
        r["cif_nif_cliente"],
        # r["cliente_fis_jur"],
        # r["cod_escivil"],
        # r["cliente_fis_jur"],
        # valida_fecha(r["fecha_alta_cliente"]),
        r["nombre_cliente"],
        # r["dir_cliente"],
        # r["cp_cliente"],
        # r["poblacion_cliente"],
        # r["cod_provincia"],
        # r["cod_sexo"],
        # valida_fecha(r["fecha_baja_cliente"]),
        # valida_fecha(r["fecha_naci_cliente"]),
        r["telefono"],
        sep='; ', end='\n')

# Fn insertar datos en lista
def insertar_cliente_lista(r):
    clientesPaccList.append((
        valida_nif(r["cif_nif_cliente"], r["cod_cliente"]), 
        valida_cadena(r["nombre_cliente"],150),
        valida_cadena(r["nombre"],45), 
        valida_cadena(r["apellido1"],45),
        valida_cadena(r["apellido2"],45),
        valida_cadena(r["dir_cliente"],45),
        valida_cadena(r["cp_cliente"],5),
        valida_cadena(r["poblacion_cliente"],30),
        valida_entero(r["cod_provincia"]),
        valida_telefono(r["telefono"]),         #telefono
        valida_telefono(r["telefono"], True),   #movil
        valida_fecha(r["fecha_naci_cliente"]),  
        valida_fecha(r["fecha_carnet"]), 
        valida_persona(r["cliente_fis_jur"]),   #persona fisica juridica
        valida_ecivil(r["cod_escivil"]),        #estado civil       
        'now()',                                #fecha alta 
        sucursal,                               #sucursal
        colaborador,                            #colaborador
        'now()',                                #create_at
        tag,                                    #tag
        ''                                      #passweb
        ))

# Fn insertar datos en lista
def insertar_cliente_codnif_lista(r):
    if r["cif_nif_cliente"] is None:
        return
    clientesCodNifList.append((
        r["cod_cliente"],
        r["cif_nif_cliente"], 
        ))

# Fn recuperar nif a partir de codigo cliente
def getNif(cod_cliente):
    cod_cliente = int(cod_cliente)
    try:
        return clientesCodNifListDict[cod_cliente]
    except KeyError:
        # prRed(f"ERR: NO EXISTE EL COD_CLIENTE {cod_cliente}")
        return ''

# Fn equivalencia ramos pacc
def getRamoPacc(a,b,c):
    return '614'

# Fn ver datos por pantalla
def ver_datos_polizas(r):
    print(
        valida_cadena(r["cod_poliza_cia"],24),              # cia poliza
        getCodCia(r["cia_poliza"]),                         # compania
        getRamoPacc(r["producto"],r["ramo"],r["descripcion_pro"]),   # producto
        valida_fecha(r["fecha_efecto"]),                    # fecha efecto    
        valida_fecha(r["pro_vto_rec"]),                     # fecha vencimiento
        getSituacion(r["estado"]),                          # situacion
        getNif(r["n_cliente"]),                             # nif
        '',                                                 # nif asegurado
        False,                                              # ase_es_asegurado
        r['matricula'],                                     # matricula
        r["forma_pago"][0:3],                               # forma pago
        tipo_poliza,                                        # tipo poliza
        'x',                                                # objeto
        'xxx',                                              # comentario
        'now()',                                            # fecha alta
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion sis
        getMotivoAnulacion(r["estado"]),                    # motivo anulacion
        canal,                                              # canal
        valida_cadena('-vacio-',24),                        # iban
        sucursal,                                           # sucursal
        colaborador,                                        # colaborador
        tag,                                                # tag
        sep='; ', end='\n\n')

# Fn capturar contador y añadir ceros a la izquierda
def getNewContrato():
    contrato = ''
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM incrementa_contador('SOLICITUDPOL')")
        contrato = sucursal + str(cur.fetchone()[0]).zfill(8)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return contrato

# Fn insertar datos en lista
def insertar_poliza_lista(r):
    polizasPaccList.append((
        getNewContrato(),
        valida_cadena(r["cod_poliza_cia"],24),              # cia poliza
        getCodCia(r["cia_poliza"]),                         # compania
        getRamoPacc(r["producto"],r["ramo"],r["descripcion_pro"]),   # producto
        valida_fecha(r["fecha_efecto"]),                    # fecha efecto    
        valida_fecha(r["pro_vto_rec"]),                     # fecha vencimiento
        getSituacion(r["estado"]),                          # situacion
        getNif(r["n_cliente"]),                             # nif
        '',                                                 # nif asegurado
        False,                                              # ase_es_asegurado
        valida_cadena(r['matricula'],15),                                     # matricula
        r["forma_pago"][0:3],                               # forma pago
        tipo_poliza,                                        # tipo poliza
        'x',                                                # objeto
        'xxx',                                              # comentario
        'now()',                                            # fecha alta
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion sis
        getMotivoAnulacion(r["estado"]),                    # motivo anulacion
        canal,                                              # canal
        '-vacio-',                                          # iban
        sucursal,                                           # sucursal
        colaborador,                                        # colaborador
        tag, 
        ))

# Fn insertar cliente
def insertar_clientes_bd():
    sql = """INSERT INTO clientes(nif,nombre,cli_nombre,cli_apellido1,cli_apellido2,domicilio,cpostal,poblacion,provincia,tel_privado,movil,fecha_nacimiento,fecha_carnet,persona,ecivil,fecha_alta,sucursal,colaborador,created_at,tag,passweb)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT ON CONSTRAINT clientes_pk 
                DO NOTHING"""
    
    vendor_id = None
    try:
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, clientesPaccList)
        cur.executemany("INSERT INTO relacion_codigo_cliente_nif VALUES(%s,%s)", clientesCodNifList)
        cur.execute("UPDATE clientes SET nombre2 = nombre, domicilio2 = domicilio, poblacion2 = poblacion, cpostal2 = cpostal, provincia2 = provincia WHERE tag = 'INI'")
        # get the generated id back
        # vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return vendor_id

# Fn insertar cliente
def insertar_polizas_bd():
    sql = """INSERT INTO polizas 
            (poliza,cia_poliza,compania,producto,fecha_efecto,fecha_vencimiento,situacion,nif,nif_asegurado,ase_es_asegurado,matricula,forma_pago,
            tipo_poliza,objeto,comentario,fecha_alta,fecha_anula,fecha_anula_sis,causa_anula,canal,iban,sucursal,colaborador,tag) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        cur = conn.cursor()
        cur.executemany(sql, polizasPaccList)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return 
   

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Variables
sucursal = '2901'
colaborador = '29010001'
tag = 'INI'
tipo_poliza = 1
canal = 6
path_files = 'datos/'
path_files = 'CTM/BBDD/'

# read database configuration
params = config()
# connect to the PostgreSQL database
conn = psycopg2.connect(**params)
### temporal ###
borrar_datos()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  CLIENTES

# Lectura fichero con multiples JSON
clientesList = []
with open(path_files + 'eb_clientes.txt', encoding="utf8") as f:
    for jsonObj in f:
        resourceDict = json.loads(jsonObj)
        clientesList.append(resourceDict)

# Ver nombres columnas
# print('\n'.join(list(resourceDict.keys())))

# Bucle clientes
clientesPaccList = []
clientesCodNifList = []
for r in clientesList:
    # ver_datos(r)
    insertar_cliente_lista(r)
    insertar_cliente_codnif_lista(r)

# Ver datos
# print('\n',clientesPaccList)

clientesCodNifListDict = dict(clientesCodNifList)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  POLIZAS

# Lectura fichero con multiples JSON
polizasList = []
with open(path_files + 'eb_polizas.txt', encoding="utf8") as f:
    for jsonObj in f:
        resourceDict = json.loads(jsonObj)
        polizasList.append(resourceDict)

# Ver nombres columnas
# print('\n'.join(list(resourceDict.keys())))

# Bucle polizas
polizasPaccList = []
for r in polizasList:
    # ver_datos_polizas(r)
    insertar_poliza_lista(r)

# Ver datos
# print('\n',polizasPaccList)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  PROCESAR

# Insertar bd
insertar_clientes_bd()
insertar_polizas_bd()
# Cerrar conexion
if conn is not None:
    conn.close()

# Mensaje fin proceso
prGreen('Success!')
