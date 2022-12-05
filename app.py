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
    cur.execute(f"DELETE FROM recibos WHERE created_by = '{created_by}'")
    conn.commit()
    cur.close()

    prYellow('>> Borrado completado')

def get_nif(cod_cliente):

    for d in clientesList:
        if d["cod_cliente"] == int(cod_cliente):
            if d["cif_nif_cliente"] is not None:
                return d["cif_nif_cliente"]
    
    return str(cod_cliente).zfill(9)

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

def get_nuevo_recibo():
    recibo = ''
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM incrementa_contador('RECIBO')")
        recibo = sucursal + str(cur.fetchone()[0]).zfill(7)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return recibo

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

def values_poliza(contrato, r):
    
    return (
        contrato,
        valida_cadena(r["cod_poliza_cia"], 24),              # cia poliza
        getCodCia(r["cia_poliza"]),                         # compania
        get_ramo_pacc(r["producto"]),                       # producto
        valida_fecha(r["fecha_efecto"]),                    # fecha efecto
        valida_fecha(r["pro_vto_rec"]),                     # fecha vencimiento
        getSituacion(r["estado"]),                          # situacion
        get_nif(r["n_cliente"]),                            # nif
        '',                                                 # nif asegurado
        False,                                              # ase_es_asegurado
        valida_cadena(r['matricula'], 15),                   # matricula
        r["forma_pago"][0:3],                               # forma pago
        tipo_poliza,                                        # tipo poliza
        r['riesgo'],                                        # objeto
        get_comentario(r),                                  # comentario
        'now()',                                            # fecha alta
        valida_fecha(r["fecha_anulacion"]),                 # fecha anulacion
        # fecha anulacion sis
        valida_fecha(r["fecha_anulacion"]),
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

def values_pol_autos(contrato, r_pol_auto):
    return (
        contrato,
        r_pol_auto["marca"],
        r_pol_auto["modelo"],
        get_clase_auto(r_pol_auto["clase"]),
        get_uso_auto(r_pol_auto["uso"]),
        valida_fecha(r_pol_auto["fecha_1_matri"]),
        created_by,
    )

def get_datos_poliza(cod_poliza):

    for d in polizasList:
        if d["cod_poliza"] == int(cod_poliza):
            return values_poliza(d["contrato_pacc"], d)
    
    return []

def insertar_recibo_bd(r):
    
    datos_poliza = get_datos_poliza(r["cod_poliza"])
    if datos_poliza == []:
        return

    cia_recibo = r["num_recibo"] if r["num_recibo"] is not None else ''
    situacion = 206

    sql = """INSERT INTO recibos 
            (poliza,cia_poliza,recibo,cia_recibo,compania,producto,tipo,nif,iban,colaborador,canal,situacion,prima_tarifa,prima_neta,prima_total,
            fecha_emision,fecha_efecto,fecha_vencimiento,sucursal,created_by) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    
    values = (
        datos_poliza[0],                                        # contrato
        r["cod_poliza_cia"],                                    # cia_poliza
        get_nuevo_recibo(),                                     # recibo
        valida_cadena(cia_recibo, 20),                          # cia_recibo
        datos_poliza[2],            # compania
        datos_poliza[3],            # producto
        r["clase_recibo"][0],
        datos_poliza[6],            # nif
        datos_poliza[9],           # iban
        colaborador,
        canal,
        situacion,
        r["prima_neta"],
        r["prima_neta"],
        r["prima_total"],
        valida_fecha(r["fecha_emision"]),
        valida_fecha(r["fecha_vto1"]),
        valida_fecha(r["fecha_vto2"]),
        sucursal,
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

def insertar_docu_bd(r):

    # Solo polizas y clientes
    if r["grupo"] not in [1, 3]:
        return

    fecha = valida_fecha(r["fecha"])
    grupo = get_carpeta_grupo(r["grupo"])
    fichero = r["fichero"]

    # [ Copiar fichero ]
    path_origen = f'D:/TRABAJO/PACTREBOL/CTM/Documentos/{grupo}/{("/").join(str(r["codigo"]))}/{fichero}'
    path_destino = f'{os.path.dirname(__file__)}/__pactrebol_documentos/{fecha.replace("-","/")[:8]}'

    # Verificar existencia fichero
    # if not os.path.exists(path_origen):
        # prRed(f'El fichero origen {path_origen} no existe')
        # docuNoExisteList.append(path_origen)
        # return None

    # Crear carpetas
    if not os.path.exists(path_destino):
        os.makedirs(path_destino, exist_ok=True)

    # Copiar fichero
    # shutil.copyfile(path_origen, path_destino + "/" + fichero)

    # [ Insertar registro ]
    cliente = poliza = ''
    if r["grupo"] == 1:
        cliente = get_nif(r["cod_regis_tabla"])
    elif r["grupo"] == 3:
        datos_poliza = get_datos_poliza(r["cod_regis_tabla"])
        if datos_poliza != []:
            poliza = datos_poliza[0]
        
    if cliente == '' and poliza == '':
        return

    sql = """INSERT INTO documentos (nif,poliza,ruta,fecha_alta,descripcion,created_by) 
            VALUES (%s,%s,%s,%s,%s,%s)"""

    values = (
        cliente,
        poliza,
        fichero,
        fecha,
        valida_cadena(r["descripcion"], 50),
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

def insertar_poliza_bd(r):

    contrato = get_nuevo_contrato()

    sql_poliza = """INSERT INTO polizas 
            (poliza,cia_poliza,compania,producto,fecha_efecto,fecha_vencimiento,situacion,nif,nif_asegurado,ase_es_asegurado,matricula,forma_pago,
            tipo_poliza,objeto,comentario,fecha_alta,fecha_anula,fecha_anula_sis,causa_anula,canal,iban,sucursal,colaborador,created_by) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING poliza"""

    sql_poliza_autos = """INSERT INTO polizas_autos 
            (poliza,marca,modelo,clase,uso,fecha_matriculacion,created_by) 
            VALUES (%s,%s,%s,%s,%s,%s,%s)"""

    try:
        cur = conn.cursor()
        # Verificar existencia de la poliza
        cur.execute(
            "select exists (select 1 from polizas where cia_poliza = %s)", (r["cod_poliza_cia"],))
        if cur.fetchone()[0]:
            prRed(f'La póliza {r["cod_poliza_cia"]} ya existe')
        else:
            # prLightPurple(f'Se graba poliza {r["cod_poliza_cia"]}')
            cur.execute(sql_poliza, values_poliza(contrato, r))
            contrato = cur.fetchone()[0]
            # if contrato: polizasCodigosList.append(f"{r['cod_poliza']};{';'.join([str(x) for x in values_pol])}".replace('\n', ''))
            # Insertar en pol_autos
            r_pol_auto = get_datos_polizas_autos(r["cod_poliza"])
            if contrato and r_pol_auto:
                cur.execute(sql_poliza_autos, values_pol_autos(contrato, r_pol_auto))

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return contrato

def insertar_cliente_bd(r):
    
    sql_cliente = """INSERT INTO clientes(nif,nombre,cli_nombre,cli_apellido1,cli_apellido2,domicilio,cpostal,poblacion,provincia,tel_privado,movil,fecha_nacimiento,fecha_carnet,persona,ecivil,nombre2,domicilio2,poblacion2,cpostal2,provincia2,fecha_alta,sucursal,colaborador,created_at,created_by,passweb)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT ON CONSTRAINT clientes_pk 
        DO NOTHING"""

    nif = valida_nif(r["cif_nif_cliente"], r["cod_cliente"])

    values_cliente = (
        nif,
        valida_cadena(r["nombre_cliente"], 150),
        valida_cadena(r["nombre"], 45),
        valida_cadena(r["apellido1"], 45),
        valida_cadena(r["apellido2"], 45),
        valida_cadena(r["dir_cliente"], 45),
        valida_cadena(r["cp_cliente"], 5),
        valida_cadena(r["poblacion_cliente"], 30),
        valida_entero(r["cod_provincia"]),
        valida_telefono(r["telefono"]),  # telefono
        valida_telefono(r["telefono"], True),  # movil
        valida_fecha(r["fecha_naci_cliente"]),
        valida_fecha(r["fecha_carnet"]),
        valida_persona(r["cliente_fis_jur"]),  # persona fisica juridica
        valida_ecivil(r["cod_escivil"]),  # estado civil
        valida_cadena(r["nombre"], 45),
        valida_cadena(r["dir_cliente"], 45),
        valida_cadena(r["poblacion_cliente"], 30),
        valida_cadena(r["cp_cliente"], 5),
        valida_entero(r["cod_provincia"]),
        'now()',  # fecha alta
        sucursal,  # sucursal
        colaborador,  # colaborador
        'now()',  # create_at
        created_by,  # created_by
        ''  # passweb
    )

    try:
        cur = conn.cursor()
        # Insertar en clientes
        cur.execute("select exists (select 1 from clientes where nif = %s)", (nif,))
        if not cur.fetchone()[0]:
            cur.execute(sql_cliente, values_cliente)
            conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# INIT

sucursal = '2901'
colaborador = '29010001'
created_by = 'ebroker'
tipo_poliza = 1
canal = 6

# read database configuration
params = config()
# connect to the PostgreSQL database
conn = psycopg2.connect(**params)

# read setting
setting = config('database.ini', 'setting')
path_files = setting["path_files"]

# borrar datos en ambiente develop
if setting["borrar_datos_bd"]:
    borrar_datos()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  VARIOS

prCyan('>> Importar tablas')
polizasAutosList = importFile('polizas_autos')
clasesAutosList = importFile('clases_autos')
polizasGarantiasList = importFile('pol_garantias')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  CLIENTES

prCyan('>> Importar clientes')
clientesList = importFile('clientes')
for r in clientesList: insertar_cliente_bd(r)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  POLIZAS

prCyan('>> Importar Polizas')
polizasList = importFile('polizas')
for i,r in enumerate(polizasList): 
    polizasList[i]["contrato_pacc"] = insertar_poliza_bd(r)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  RECIBOS

prCyan('>> Importar Recibos')
recibosList = importFile('recibos')
for r in recibosList: insertar_recibo_bd(r)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  DOCUMENTOS

prCyan('>> Importar Docs')
docusList = importFile('docu')
for r in docusList: insertar_docu_bd(r)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  FIN

# Cerrar conexion
if conn is not None:
    conn.close()

# Mensaje fin proceso
prGreen('Success!')