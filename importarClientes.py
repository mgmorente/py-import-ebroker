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
    cur.execute(f"DELETE FROM clientes WHERE created_by = '{created_by}'")
    cur.execute(f"DELETE FROM polizas WHERE created_by = '{created_by}'")
    cur.execute(f"DELETE FROM polizas_autos WHERE created_by = '{created_by}'")
    cur.execute(f"DELETE FROM relacion_codigo_cliente_nif")
    conn.commit()
    cur.close()

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
        created_by,                                    #created_by
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
def get_nif(cod_cliente):
    cod_cliente = int(cod_cliente)
    try:
        return clientesCodNifListDict[cod_cliente]
    except KeyError:
        # prRed(f"ERR: NO EXISTE EL COD_CLIENTE {cod_cliente}")
        return str(cod_cliente).zfill(9)

# Fn equivalencia ramos pacc
def get_ramo_pacc(cod_ramo):
    if cod_ramo == '10101':
        return 614
    
    return 0

# Fn capturar contador y añadir ceros a la izquierda
def get_nuevo_contrato():
    contrato = ''
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM incrementa_contador('SOLICITUDPOL')")
        contrato = sucursal + str(cur.fetchone()[0]).zfill(8)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return contrato

# Extraer datos del cliente de la lista
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

def get_comentario(r):
    
    comentario = '\n[PRO] ' + r["descripcion_pro"] 
    
    for i, t in enumerate(polizasGarantiasList):
        if t["cod_poliza"] == r["cod_poliza"] and t["marca"] == 'S':
            # print(polizasGarantiasList[i])
            comentario += '\n[GAR] ' + t["descripcion"]
            if t["capital"]:
                comentario += f' (Capital: {t["capital"]})'

    comentario += '\n[COD] ' + str(r["cod_poliza"])

    return comentario
    
def get_iban(r):
    if r["entidad_bancaria"] is None or r["num_cuenta_poliza"] is None:
        return ''
    else:
        return r["entidad_bancaria"] + r["ofi_banco_poliza"] + r["co_banco_poliza"] + r["num_cuenta_poliza"]
    
def values_poliza(r):
    return (
        get_nuevo_contrato(),
        valida_cadena(r["cod_poliza_cia"],24),              # cia poliza
        getCodCia(r["cia_poliza"]),                         # compania
        get_ramo_pacc(r["producto"]),                       # producto
        valida_fecha(r["fecha_efecto"]),                    # fecha efecto    
        valida_fecha(r["pro_vto_rec"]),                     # fecha vencimiento
        getSituacion(r["estado"]),                          # situacion
        get_nif(r["n_cliente"]),                            # nif
        '',                                                 # nif asegurado
        False,                                              # ase_es_asegurado
        valida_cadena(r['matricula'],15),                   # matricula
        r["forma_pago"][0:3],                               # forma pago
        tipo_poliza,                                        # tipo poliza
        r['riesgo'],                                        # objeto
        get_comentario(r),                                  # comentario
        'now()',                                            # fecha alta
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion sis
        getMotivoAnulacion(r["estado"]),                    # motivo anulacion
        canal,                                              # canal
        get_iban(r),                                        # iban
        sucursal,                                           # sucursal
        colaborador,                                        # colaborador
        created_by, 
        )

def get_datos_polizas_autos(cod_poliza):
    list = []
    for r_pol_auto in polizasAutosList:
        if r_pol_auto["cod_poliza"] == r["cod_poliza"]:
            # print(r_pol_auto["clase"],r_pol_auto["uso"],r_pol_auto["matricula"])
            return r_pol_auto

def get_clase_auto(codigo):
    
    # 1 ,  "TURISMO" 1 
    # 2 ,  "FURGONETA"  3
    # 3 ,  "CAMION RIGIDO"  10
    # 4 ,  "CICLOMOTOR"  34
    # 5 ,  "MOTOCICLETA"  30
    # 6 ,  "REMOLQUE"  38
    # 7 ,  "TRACTORES"  40
    # 8 ,  "M. AGRICOLA"  
    # 9 ,  "VEHICULO IND." 15  
    # 10 , "C.TRACTORA"  23
    # 11 , "FURG. < 700"  7
    # 12 , "FURG. > 700"  7
    # 13 , "MOTOCULTOR"  27
    # 14 , "MOTOCARRO"  
    # 15 , "AUTOBUS"  29
    list = [
        (1,1),
        (2,3),
        (3,10),
        (4,34),
        (5,30),
        (6,38),
        (7,40),
        (8,0),
        (9,15),
        (10,23),
        (11,7),
        (12,7),
        (13,27),
        (14,0),
        (15,29),
        ]

    if codigo is None or  not 1 >= int(codigo) <=len(list):
        return 0
    else:
        return list[codigo-1][1]

def get_uso_auto(codigo):
    
    # 1 : "PARTICULAR" 1
    # 2 : "PLAR/TTES PROPIOS" 18
    # 3 : "TTES.PROPIOS" 
    # 4 : "TTES.PROPIOS TIR" 
    # 5 : "ALQUILER SIN COND." 7
    # 6 : "ALQUILER CON COND." 7
    # 7 : "S.P.SIN TAXIMETRO" 4
    # 8 : "S.P.CON TAX.C.PRO" 4
    # 9 : "S.P.CON TAX.C.EMP" 4
    # 10 : "S.P." 2
    # 11 : "S.P.> 300" 2
    # 12 : "S.P.< 300 TIR"  2
    # 13 : "S.P.< 300" 2
    # 14 : "S.P.> 300 TIR" 2
    # 15 : "VEHICULO COLECCION"  
    # 16 : "AMBULANCIA" 
    # 17 : "AUTOESCUELA" 8
    # 18 : "DISCRECIONAL" 
    # 19 : "LINEA REGULAR" 
    # 20 : "URBANO" 0
    # 21 : "POLICIA " 0
    # 22 : "CAMION BASURA " 0
    list = [
        (1,1),
        (2,18),
        (3,0),
        (4,0),
        (5,7),
        (6,7),
        (7,4),
        (8,4),
        (9,4),
        (10,2),
        (11,2),
        (12,2),
        (13,2),
        (14,2),
        (15,0),
        (16,0),
        (17,8),
        (18,0),
        (19,0),
        (20,0),
        (21,0),
        (22,0),
        ]

    if codigo is None or  not 1 >= int(codigo) <=len(list):
        return 0
    else:
        return list[codigo-1][1]

def values_pol_autos(contrato,r_pol_auto):
    return (
        contrato, 
        r_pol_auto["marca"], 
        r_pol_auto["modelo"], 
        get_clase_auto(r_pol_auto["clase"]), 
        get_uso_auto(r_pol_auto["uso"]),
        valida_fecha(r_pol_auto["fecha_1_matri"]),
        created_by,
        )

def insertar_poliza_bd(r):

    sql_poliza = """INSERT INTO polizas 
            (poliza,cia_poliza,compania,producto,fecha_efecto,fecha_vencimiento,situacion,nif,nif_asegurado,ase_es_asegurado,matricula,forma_pago,
            tipo_poliza,objeto,comentario,fecha_alta,fecha_anula,fecha_anula_sis,causa_anula,canal,iban,sucursal,colaborador,created_by) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING poliza"""
    
    sql_poliza_autos = """INSERT INTO polizas_autos 
            (poliza,marca,modelo,clase,uso,fecha_matriculacion,created_by) 
            VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    
    sql_cliente = """INSERT INTO clientes(nif,nombre,cli_nombre,cli_apellido1,cli_apellido2,domicilio,cpostal,poblacion,provincia,tel_privado,movil,fecha_nacimiento,fecha_carnet,persona,ecivil,nombre2,domicilio2,poblacion2,cpostal2,provincia2,fecha_alta,sucursal,colaborador,created_at,created_by,passweb)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT ON CONSTRAINT clientes_pk 
                DO NOTHING"""

    try:
        cur = conn.cursor()
        # Verificar existencia de la poliza
        cur.execute("select exists (select 1 from polizas where cia_poliza = %s)", (r["cod_poliza_cia"],))
        if not cur.fetchone()[0]:
            # prLightPurple(f'Se graba poliza {r["cod_poliza_cia"]}')
            
            # Insertar en polizas
            cur.execute(sql_poliza, values_poliza(r))
            contrato = cur.fetchone()[0]
            
            # Insertar en pol_autos
            r_pol_auto = get_datos_polizas_autos(r["cod_poliza"])
            if contrato and r_pol_auto:
                cur.execute(sql_poliza_autos, values_pol_autos(contrato,r_pol_auto))
            
            # Insertar en clientes
            cur.execute("select exists (select 1 from clientes where nif = %s)", (get_nif(r["n_cliente"]),))
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

def importFile(name):
    list = []
    with open(f'{path_files}/eb_{name}.txt', encoding="utf8") as f:
        for jsonObj in f:
            resourceDict = json.loads(jsonObj)
            list.append(resourceDict)
    
    return list

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Variables
sucursal = '2901'
colaborador = '29010001'
created_by = 'ebroker'
tipo_poliza = 1
canal = 6
path_files = 'datos'
path_files = 'CTM/BBDD'

# read database configuration
params = config()
# connect to the PostgreSQL database
conn = psycopg2.connect(**params)

# # # QUITAR # # #
borrar_datos()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  VARIOS

polizasAutosList = importFile('polizas_autos')
clasesAutosList = importFile('clases_autos')
polizasGarantiasList = importFile('pol_garantias')
# print('\n'.join(list(resourceDict.keys())))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  CLIENTES

# Lectura fichero con multiples JSON
clientesList = importFile('clientes')

# Bucle clientes
clientesPaccList = []
clientesCodNifList = []
for r in clientesList:
    # ver_datos(r)
    insertar_cliente_lista(r)
    insertar_cliente_codnif_lista(r)

clientesCodNifListDict = dict(clientesCodNifList)

# Localizar fila cliente
# fila = [d for d in clientesPaccList if d[0] == '10740618D']
# prRed(fila)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  POLIZAS

# Lectura fichero con multiples JSON
polizasList = []
with open(path_files + '/eb_polizas.txt', encoding="utf8") as f:
    for jsonObj in f:
        resourceDict = json.loads(jsonObj)
        polizasList.append(resourceDict)

# Bucle polizas
polizasPaccList = []
for r in polizasList:
    insertar_poliza_bd(r)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  FIN

# Cerrar conexion
if conn is not None:
    conn.close()

# Mensaje fin proceso
prGreen('Success!')
