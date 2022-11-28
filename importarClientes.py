import json
import psycopg2
from config import config
from utils import *

# Fn borrar datos y tablas
def borrar_datos():
    cur = conn.cursor()
    # Crear tabla relacion codigo cliente nif
    sql = '''CREATE TABLE IF NOT EXISTS public.relacion_codigo_cliente_nif(
    codigo integer NOT NULL,
    nif character varying(12) COLLATE pg_catalog."default" NOT NULL DEFAULT ''::character varying,
    CONSTRAINT codigo_pk PRIMARY KEY (codigo))'''
    cur.execute(sql)
    # Borrar tablas
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
        valida_cadena(r["nombre"],45), 
        valida_cadena(r["dir_cliente"],45),
        valida_cadena(r["poblacion_cliente"],30),
        valida_cadena(r["cp_cliente"],5),
        valida_entero(r["cod_provincia"]),
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
        return str(cod_cliente).zfill(9)

# Fn equivalencia ramos pacc
def getRamoPacc(cod_ramo):
    if cod_ramo == '10101':
        return 614
    
    return 0

# Fn ver datos por pantalla
# def ver_datos_polizas(r):
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
# def insertar_poliza_lista(r):
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
        valida_cadena(r['matricula'],15),                   # matricula
        r["forma_pago"][0:3],                               # forma pago
        tipo_poliza,                                        # tipo poliza
        '--',                                               # objeto
        '--',                                               # comentario
        'now()',                                            # fecha alta
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion sis
        getMotivoAnulacion(r["estado"]),                    # motivo anulacion
        canal,                                              # canal
        '--',                                               # iban
        sucursal,                                           # sucursal
        colaborador,                                        # colaborador
        tag, 
        ))

# Fn insertar cliente
# def insertar_clientes_bd():
    prCyan('>> Se insertan datos en clientes')

    sql = """INSERT INTO clientes(nif,nombre,cli_nombre,cli_apellido1,cli_apellido2,domicilio,cpostal,poblacion,provincia,tel_privado,movil,fecha_nacimiento,fecha_carnet,persona,ecivil,fecha_alta,sucursal,colaborador,created_at,tag,passweb)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT ON CONSTRAINT clientes_pk 
                DO NOTHING"""
    try:
        cur = conn.cursor()
        cur.executemany(sql, clientesPaccList)
        cur.executemany("INSERT INTO relacion_codigo_cliente_nif VALUES(%s,%s)", clientesCodNifList)
        cur.execute("UPDATE clientes SET nombre2 = substring(nombre,0,45), domicilio2 = domicilio, poblacion2 = poblacion, cpostal2 = cpostal, provincia2 = provincia WHERE tag = 'INI'")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return 

# Fn insertar polizas
# def insertar_polizas_bd():
    prCyan('>> Se insertan datos en polizas')

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

def datos_clientes_pacc(cod_cliente):
    # Localizar nif en relacion codigocliente-nif
    rowCodNif = [d for d in clientesCodNifList if d[0] == cod_cliente]
    if rowCodNif:
        nif = rowCodNif[0][1]
    else:
        nif = cod_cliente 

    # Localizar indice del cliente en la lista cliente
    for i, t in enumerate(clientesPaccList):
        if t[0] == nif:
            return clientesPaccList[i]

    return None            
    
        
def insertar_poliza_bd(r):
    # print( r["producto"], ' >> ', r["ramo"], ' >> ',r["descripcion_pro"]),   # producto
    values = (
        getNewContrato(),
        valida_cadena(r["cod_poliza_cia"],24),              # cia poliza
        getCodCia(r["cia_poliza"]),                         # compania
        getRamoPacc(r["producto"]),                         # producto
        valida_fecha(r["fecha_efecto"]),                    # fecha efecto    
        valida_fecha(r["pro_vto_rec"]),                     # fecha vencimiento
        getSituacion(r["estado"]),                          # situacion
        getNif(r["n_cliente"]),                             # nif
        '',                                                 # nif asegurado
        False,                                              # ase_es_asegurado
        valida_cadena(r['matricula'],15),                   # matricula
        r["forma_pago"][0:3],                               # forma pago
        tipo_poliza,                                        # tipo poliza
        '--',                                               # objeto
        '--',                                               # comentario
        'now()',                                            # fecha alta
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion sis
        getMotivoAnulacion(r["estado"]),                    # motivo anulacion
        canal,                                              # canal
        '--',                                               # iban
        sucursal,                                           # sucursal
        colaborador,                                        # colaborador
        tag, 
        )

    sql_poliza = """INSERT INTO polizas 
            (poliza,cia_poliza,compania,producto,fecha_efecto,fecha_vencimiento,situacion,nif,nif_asegurado,ase_es_asegurado,matricula,forma_pago,
            tipo_poliza,objeto,comentario,fecha_alta,fecha_anula,fecha_anula_sis,causa_anula,canal,iban,sucursal,colaborador,tag) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING poliza"""
    
    sql_poliza_autos = """INSERT INTO polizas_autos 
            (poliza,marca,modelo) 
            VALUES (%s,%s,%s)"""
    
    sql_cliente = """INSERT INTO clientes(nif,nombre,cli_nombre,cli_apellido1,cli_apellido2,domicilio,cpostal,poblacion,provincia,tel_privado,movil,fecha_nacimiento,fecha_carnet,persona,ecivil,nombre2,domicilio2,poblacion2,cpostal2,provincia2,fecha_alta,sucursal,colaborador,created_at,tag,passweb)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT ON CONSTRAINT clientes_pk 
                DO NOTHING"""

    try:
        cur = conn.cursor()
        # Verificar existencia de la poliza
        cur.execute("select exists (select 1 from polizas where cia_poliza = %s)", (r["cod_poliza_cia"],))
        if not cur.fetchone()[0]:
            # prLightPurple(f'Se graba poliza {r["cod_poliza_cia"]}')
            cur.execute(sql_poliza, values)
            contrato = cur.fetchone()[0]
            if contrato:
                # Si es de tipo auto capturamos datos del fichero polizas autos
                for r_pol_auto in polizasAutosList:
                    if r_pol_auto["cod_poliza"] == r["cod_poliza"]:
                        cur.execute(sql_poliza_autos, (contrato, r_pol_auto["marca"], r_pol_auto["modelo"]))
                        # print(r_pol_auto["marca"],r_pol_auto["clase"],r_pol_auto["valor"],r_pol_auto["modelo"],r_pol_auto["uso"],r_pol_auto["matricula"])

                # Verificar existencia del cliente
                cur.execute("select exists (select 1 from clientes where nif = %s)", (getNif(r["n_cliente"]),))
                if not cur.fetchone()[0]:
                    # Capturar datos del cliente
                    values_cliente = datos_clientes_pacc(r["n_cliente"])
                    if values_cliente:
                        # prRed(f'Se graba cliente {r["cod_poliza_cia"]}')
                        cur.execute(sql_cliente, values_cliente)

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
# path_files = 'CTM/BBDD/'

# read database configuration
params = config()
# connect to the PostgreSQL database
conn = psycopg2.connect(**params)
### temporal ###
borrar_datos()



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  VARIOS

polizasAutosList = []
with open(path_files + 'eb_polizas_autos.txt', encoding="utf8") as f:
    for jsonObj in f:
        resourceDict = json.loads(jsonObj)
        polizasAutosList.append(resourceDict)

# print('\n'.join(list(resourceDict.keys())))


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

# Localizar fila cliente
# fila = [d for d in clientesPaccList if d[0] == '10740618D']
# prRed(fila)

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
    # insertar_poliza_lista(r)
    insertar_poliza_bd(r)

# Ver datos
# print('\n',polizasPaccList)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  PROCESAR

# Insertar bd
# insertar_clientes_bd()
# insertar_polizas_bd()
# Cerrar conexion
if conn is not None:
    conn.close()

# Mensaje fin proceso
prGreen('Success!')
