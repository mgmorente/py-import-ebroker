import json
import os
import psycopg2
from config import config
from utils import *
import shutil

# Fn borrar datos y tablas
def borrar_datos():
    cur = conn.cursor()
    cur.execute(f"DELETE FROM clientes WHERE created_by = '{created_by}'")
    cur.execute(f"DELETE FROM polizas WHERE created_by = '{created_by}'")
    cur.execute(f"DELETE FROM polizas_autos WHERE created_by = '{created_by}'")
    cur.execute(f"DELETE FROM documentos WHERE created_by = '{created_by}'")
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
    if cod_ramo == '21703': return 604 # S.O.ACT.NAUTICAS
    elif cod_ramo == '20901': return 302 # GASTOS REEMBOL.
    elif cod_ramo == '20902': return 305 # GASTOS CONCERT.
    elif cod_ramo == '20903': return 305 # MIXTO REEM-CON.
    elif cod_ramo == '20701': return 101 # ACC.INDIVIDUAL
    elif cod_ramo == '20702': return 701 # ACC.COLECTIVOS
    elif cod_ramo == '20703': return 700 # ACC.CONV.LABOR.
    elif cod_ramo == '20704': return 101 # ACC.OCUP.AUTOS
    elif cod_ramo == '20806': return 207 # AGRICOLA
    elif cod_ramo == '21601': return 000 # GANADO
    elif cod_ramo == '21602': return 000 # ACUICOLAS
    elif cod_ramo == '21603': return 000 # FORESTALES
    elif cod_ramo == '21604': return 000 # CUL.HER.EXTENSIVOS
    elif cod_ramo == '21605': return 000 # FRUTALES
    elif cod_ramo == '21606': return 000 # CITRICOS
    elif cod_ramo == '21607': return 000 # PLATANO
    elif cod_ramo == '21608': return 000 # FRUTOS SECOS
    elif cod_ramo == '21609': return 000 # HORTALIZAS
    elif cod_ramo == '21610': return 000 # CUL.PROTEGIDOS
    elif cod_ramo == '21611': return 000 # PATATA
    elif cod_ramo == '21612': return 000 # CUL.INDUSTRIALES
    elif cod_ramo == '21613': return 000 # OLIVAR
    elif cod_ramo == '21614': return 000 # VI√ëEDO
    elif cod_ramo == '21615': return 000 # TARIFA GENERAL
    elif cod_ramo == '21616': return 000 # M.E.R.
    elif cod_ramo == '21617': return 000 # FRUTOS TROPICALES
    elif cod_ramo == '21201': return 212 # ASIVIA PERSONAS
    elif cod_ramo == '21202': return 220 # ASIVIA AUTOS
    elif cod_ramo == '10101': return 614 # TURISMOS/FURGO.
    elif cod_ramo == '10103': return 615 # FURGONETA >700K
    elif cod_ramo == '10104': return 614 # CUADRICICLO
    elif cod_ramo == '10201': return 601 # CAMION RIGIDO
    elif cod_ramo == '10202': return 601 # CABEZA TRACTORA
    elif cod_ramo == '10203': return 601 # REMOLQUE
    elif cod_ramo == '10204': return 618 # VEH.ESPECIAL
    elif cod_ramo == '10205': return 609 # AUTOBUS
    elif cod_ramo == '10301': return 617 # MOTOCICLETA
    elif cod_ramo == '10302': return 617 # CICLOMOTOR
    elif cod_ramo == '10303': return 614 # CUADRICICLO
    elif cod_ramo == '10304': return 617 # QUADS
    elif cod_ramo == '20603': return 126 # AVER.MAQUINARIA
    elif cod_ramo == '21501': return 800 # CAUCION
    elif cod_ramo == '20803': return 209 # COMERCIOS
    elif cod_ramo == '20802': return 203 # COMUNIDADES
    elif cod_ramo == '21401': return 802 # CREDITO
    elif cod_ramo == '21701': return 119 # CRISTALES
    elif cod_ramo == '20420': return 127 # CYBERRIESGOS
    elif cod_ramo == '20605': return 117 # S.O.DECENAL DA√ëOS
    elif cod_ramo == '21001': return 421 # DECESOS
    elif cod_ramo == '21801': return 408 # DEPENDENCIA
    elif cod_ramo == '20604': return 110 # EQUI.ELECTRONI.
    elif cod_ramo == '20801': return 201 # HOGAR
    elif cod_ramo == '20807': return 206 # HOTELES
    elif cod_ramo == '21704': return 221 # IMP.ALQUILERES
    elif cod_ramo == '20101': return 000 # INC.RIES.SENCI.
    elif cod_ramo == '20102': return 000 # INC.RIES.INDUS.
    elif cod_ramo == '21705': return 300 # MASCOTAS
    elif cod_ramo == '20804': return 204 # OFICINAS
    elif cod_ramo == '21702': return 000 # OTROS RAMOS
    elif cod_ramo == '20201': return 105 # PER.BENEFICIOS
    elif cod_ramo == '20202': return 104 # SUS.ESPECTACUL.
    elif cod_ramo == '21101': return 222 # P.J.AUTOS
    elif cod_ramo == '21102': return 222 # P.J.GENERAL
    elif cod_ramo == '20805': return 206 # P.Y.M.E.
    elif cod_ramo == '20401': return 103 # R.C.GENERAL
    elif cod_ramo == '20402': return 115 # R.C.PROFESIONAL
    elif cod_ramo == '20403': return 103 # R.C.P.NUCLEAR
    elif cod_ramo == '20404': return 108 # R.C.CAZA OBLIG.
    elif cod_ramo == '20405': return 108 # R.C.CAZA VOLUN.
    elif cod_ramo == '20406': return 103 # R.C.DECENAL
    elif cod_ramo == '20407': return 103 # R.C.EMPRESAS
    elif cod_ramo == '20408': return 102 # R.C.CONSEJEROS
    elif cod_ramo == '20409': return 509 # R.C.EMBARCA.OBLIG.
    elif cod_ramo == '20410': return 108 # R.C.PESCA OBLIG.
    elif cod_ramo == '20411': return 114 # R.C.AGRARIA
    elif cod_ramo == '20412': return 103 # R.C.DRON OBLIG.
    elif cod_ramo == '20413': return 118 # R.C.MEDIOAMBIENTAL
    elif cod_ramo == '20501': return 111 # ROBO
    elif cod_ramo == '20706': return 604 # S.O.VIAJEROS
    elif cod_ramo == '20705': return 304 # SUB.ENF.ACCID.
    elif cod_ramo == '21301': return 000 # SURECA
    elif cod_ramo == '20103': return 210 # T.R.DA√ëOS
    elif cod_ramo == '20808': return 210 # TODO RIESGO INDUSTRIAL
    elif cod_ramo == '20601': return 109 # T.R.CONSTRUCCI.
    elif cod_ramo == '20602': return 109 # T.R.MONTAJE
    elif cod_ramo == '20301': return 500 # MERCA.TERRESTR.
    elif cod_ramo == '20302': return 500 # MERCA.MARITIMO
    elif cod_ramo == '20303': return 500 # MERCA.AEREO
    elif cod_ramo == '20304': return 500 # MERCA.MIXTO
    elif cod_ramo == '20305': return 503 # CASCOS NAVEGAC.
    elif cod_ramo == '20306': return 503 # CASCOS CONSTRU.
    elif cod_ramo == '20307': return 000 # R.L.REPARADORES
    elif cod_ramo == '20308': return 509 # EMBARCA.RECREO
    elif cod_ramo == '20309': return 211 # CARAVANAS
    elif cod_ramo == '20310': return 502 # AERONAVES
    elif cod_ramo == '20311': return 503 # CASCOS P&I
    elif cod_ramo == '30108': return 422 # UNILINK
    elif cod_ramo == '30211': return 423 # UNILINK
    elif cod_ramo == '30101': return 000 # IND.DIFE.AHORRO
    elif cod_ramo == '30102': return 000 # IND.RIESGO
    elif cod_ramo == '30103': return 000 # IND.MIXTOS
    elif cod_ramo == '30104': return 000 # COL.DIFE.AHORRO
    elif cod_ramo == '30105': return 000 # COL.RIESGO
    elif cod_ramo == '30106': return 000 # COL.MIXTOS
    elif cod_ramo == '30107': return 428 # FOND.PENSIONES
    elif cod_ramo == '30109': return 406 # PPA
    elif cod_ramo == '30110': return 432 # FOND.PENSIONES RFCP
    elif cod_ramo == '30111': return 432 # FOND.PENSIONES RFLP
    elif cod_ramo == '30112': return 432 # FOND.PENSIONES RFMI
    elif cod_ramo == '30113': return 432 # FOND.PENSIONES RVMI
    elif cod_ramo == '30114': return 432 # FOND.PENSIONES RVAR
    elif cod_ramo == '30115': return 432 # FOND.PENSIONES GARA
    elif cod_ramo == '30116': return 433 # SIALP
    elif cod_ramo == '30117': return 415 # PIAS
    elif cod_ramo == '30118': return 000 # EPSV
    elif cod_ramo == '30201': return 000 # COL.AHORRO
    elif cod_ramo == '30202': return 000 # COL.RIESGO
    elif cod_ramo == '30203': return 000 # COL.MIXTOS
    elif cod_ramo == '30204': return 000 # IND.AHORRO
    elif cod_ramo == '30205': return 000 # IND.RIESGO
    elif cod_ramo == '30206': return 000 # IND.MIXTOS
    elif cod_ramo == '30207': return 425 # RENTA VITALICIA
    elif cod_ramo == '30208': return 432 # FOND.PENSIONES
    elif cod_ramo == '30209': return 000 # P.FINANCIEROS
    elif cod_ramo == '30210': return 425 # RENTAS TEMPORALES
    elif cod_ramo == '30212': return 406 # PPA
    elif cod_ramo == '30213': return 432 # FOND.PENSIONES RFCP
    elif cod_ramo == '30214': return 432 # FOND.PENSIONES RFLP
    elif cod_ramo == '30215': return 432 # FOND.PENSIONES RFMI
    elif cod_ramo == '30216': return 432 # FOND.PENSIONES RVMI
    elif cod_ramo == '30217': return 432 # FOND.PENSIONES RVAR
    elif cod_ramo == '30218': return 432 # FOND.PENSIONES GARA
    elif cod_ramo == '30219': return 433 # SIALP
    elif cod_ramo == '30220': return 415 # PIAS
    elif cod_ramo == '30221': return 000 # EPSV
    else: return 000

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
def datos_cliente_pacc(cod_cliente):
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
        if cur.fetchone()[0]:
            prRed(f'La póliza {r["cod_poliza_cia"]} ya existe')
        else:    
            # prLightPurple(f'Se graba poliza {r["cod_poliza_cia"]}')
            # Insertar en polizas
            values_pol = values_poliza(r)
            cur.execute(sql_poliza, values_pol)
            contrato = cur.fetchone()[0]

            if contrato:
                polizasCodigosList.append(f"{r['cod_poliza']};{';'.join([str(x) for x in values_pol])}".replace('\n', ''))

            # Insertar en pol_autos
            r_pol_auto = get_datos_polizas_autos(r["cod_poliza"])
            if contrato and r_pol_auto:
                cur.execute(sql_poliza_autos, values_pol_autos(contrato,r_pol_auto))
            
            # Insertar en clientes
            cur.execute("select exists (select 1 from clientes where nif = %s)", (get_nif(r["n_cliente"]),))
            if not cur.fetchone()[0]:
                # Capturar datos del cliente
                values_cliente = datos_cliente_pacc(r["n_cliente"])
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

def get_carpeta_grupo(codigo):
    if codigo == 1: return "CLIENTES".lower() 
    elif codigo == 6: return "ASEGURADORAS".lower() 
    elif codigo == 0: return "GENERAL".lower() 
    elif codigo == 3: return "POLIZAS".lower() 
    elif codigo == 14: return "PROYECTOS".lower() 
    elif codigo == 4: return "RECIBOS".lower() 
    elif codigo == 5: return "SINIESTROS".lower()

def get_cia_poliza(cod_poliza):
    for d in polizasCodigosList:
        if d[0] == cod_poliza:
            return d[1]
    
    return ''

def get_nif_cliente(cod_cliente):
    for d in clientesCodNifList:
        if d[0] == cod_cliente:
            return d[1]
    
    return ''

def insertar_docu_bd(r):
    
    # Solo polizas y clientes
    if r["grupo"] not in [1,3]: return
    
    fecha = valida_fecha(r["fecha"])
    grupo = get_carpeta_grupo(r["grupo"])
    fichero = r["fichero"]

    # [ Copiar fichero ]
    path_origen = f'C:/REPO/Python/importar_ebroker/CTM/documentos/{grupo}/{("/").join(str(r["codigo"]))}/{fichero}'
    path_destino = f'C:/xampp/htdocs/gestiondocs_ptb/ctm/documentos/{fecha.replace("-","/")[:8]}'

    # Verificar existencia fichero
    if not os.path.exists(path_origen):
        # prRed(f'El fichero origen {path_origen} no existe')
        return None

    # Crear carpetas
    if not os.path.exists(path_destino):
        os.makedirs(path_destino, exist_ok=True)

    # Copiar fichero
    shutil.copyfile(path_origen, path_destino + "/" + fichero) 

    # [ Insertar registro ]
    cliente = poliza = ''
    if r["grupo"] == 1: cliente = get_nif_cliente(r["cod_regis_tabla"])
    elif r["grupo"] == 3: poliza = get_cia_poliza(r["cod_regis_tabla"])

    if cliente == '' and poliza == '':
        return

    sql = """INSERT INTO documentos (nif,poliza,ruta,fecha_alta,descripcion,created_by) 
            VALUES (%s,%s,%s,%s,%s,%s)"""

    values = (
        cliente,
        poliza,
        fichero,
        fecha,
        valida_cadena(r["descripcion"],50),
        created_by,
    )

    try:
        cur = conn.cursor()
        cur.execute(sql, values)
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
created_by = 'ebroker'
tipo_poliza = 1
canal = 6
path_files = 'datos'
# path_files = 'CTM/BBDD'

# read database configuration
params = config()
# connect to the PostgreSQL database
conn = psycopg2.connect(**params)

# # # QUITAR # # #
prYellow('[[ATENCIÓN]] ___¿Desea borrar tablas? (S/N)')
if input().upper() == 'S':
    borrar_datos()
    prCyan('>> Borrado completado')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  VARIOS

prCyan('>> Importar tablas')
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

prCyan('>> Importar Polizas')

# Lectura fichero con multiples JSON
polizasList = importFile('polizas')

# Lista relacion cod_poliza, contrato
polizasCodigosList = []

# Bucle polizas
for r in polizasList: insertar_poliza_bd(r)

# print(polizasCodigosList)
# Exportar a fichero
absolute_path = os.path.dirname(__file__)
relative_path = "exportacion"
full_path = os.path.join(absolute_path, relative_path)
# if not os.path.exists(full_path):
#     os.makedirs(full_path, exist_ok=True)

columnas = '''cod_poliza;poliza;cia_poliza;compania;producto;fecha_efecto;fecha_vencimiento;situacion;nif;nif_asegurado;ase_es_asegurado;matricula;forma_pago;tipo_poliza;objeto;comentario;fecha_alta;fecha_anula;fecha_anula_sis;causa_anula;canal;iban;sucursal;colaborador;created_by\n'''

with open(f'{full_path}/polizas.csv', 'w+') as f:
    f.write(columnas)
    for items in polizasCodigosList:
        # line = f"{items[0]};{';'.join([str(x) for x in items[1]])}".replace('\n', '')
        f.write('%s\n' %items)
f.close()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  DOCUMENTOS

prCyan('>> Importar Docs')

# Lectura fichero con multiples JSON
docusList = importFile('docu')

# Bucle docus
for r in docusList: insertar_docu_bd(r)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#  FIN

# Cerrar conexion
if conn is not None:
    conn.close()

# Mensaje fin proceso
prGreen('Success!')
