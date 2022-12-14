from datetime import datetime
import json
from config import config

# Fn formatear fecha o devolver null
def valida_fecha(fecha = ''):
    try:
        f = datetime.strptime(fecha["$date"],"%Y-%m-%dT%H:%M:%S.000Z")
        return f.strftime("%Y-%m-%d")
    except:
        return None

# Fn validar texto y longitud
def valida_cadena(texto, longitud):
    if texto is None:
        return ''
    else:     
        return texto[0:longitud-1]

def valida_entero(numero):
    if numero is None:
        return 0
    else:
        return numero

def valida_nif(nif, codigo):
    if nif is None:
        return str(codigo).zfill(9)
    else:
        return nif

# Fn validar telefono o movil
def valida_telefono(numero, campo_movil = False):
    if numero is None:
        return ''
    
    numero = only_numerics(numero)
    if not numero:
        return ''
    
    es_numero_movil = True if int(numero[0:1]) in [6,7] else False
    if es_numero_movil and campo_movil:
        return int(numero[0:9])
    elif not es_numero_movil and not campo_movil:
        return int(numero[0:9])
    else:
        return '' 

def valida_sexo(valor):
    if valor is None:
        return ''
    
    if valor == 'M':
        return 'HOM'
    elif valor == 'F':
        return 'MUJ'
    else:
        return ''

def valida_persona(valor):
    if valor is None:
        return ''
    
    if valor == 'F':
        return 'FIS'
    elif valor == 'J':
        return 'JUR'
    else:
        return ''

def valida_ecivil(valor):
    if valor is None:
        return ''
    
    if valor == 'C': return 'CAS'
    elif valor == 'V': return 'VID'
    elif valor == 'D': return 'DIV'
    elif valor == 'S': return 'SOL' 
    elif valor == 'S': return 'SEP'
    else: return ''    

def getSituacion(valor):
    if valor is None: return 0
    if valor == "ANULADA": return 5
    else: return 1

def getMotivoAnulacion(valor):
    if valor == "ANULADA":
        return 7
    else:
        return 0    

def get_clase_auto(codigo):
 
    list = [
        (1, 1), # 1 ,  "TURISMO" 1
        (2, 3), # 2 ,  "FURGONETA"  3
        (3, 10), # 3 ,  "CAMION RIGIDO"  10
        (4, 34), # 4 ,  "CICLOMOTOR"  34
        (5, 30), # 5 ,  "MOTOCICLETA"  30
        (6, 38), # 6 ,  "REMOLQUE"  38
        (7, 40), # 7 ,  "TRACTORES"  40
        (8, 0), # 8 ,  "M. AGRICOLA"
        (9, 15), # 9 ,  "VEHICULO IND." 15
        (10, 23), # 10 , "C.TRACTORA"  23
        (11, 7), # 11 , "FURG. < 700"  7
        (12, 7), # 12 , "FURG. > 700"  7
        (13, 27), # 13 , "MOTOCULTOR"  27
        (14, 0), # 14 , "MOTOCARRO"
        (15, 29), # 15 , "AUTOBUS"  29
    ]

    if codigo is None or not 1 >= int(codigo) <= len(list):
        return 0
    else:
        return list[codigo-1][1]

def get_situacion_recibo(estado):
    if estado is None:
        return 0
    
    if  estado == "COBRADO/CIA": return 206
    elif estado == "PENDIENTE": return 106
    elif estado == "ANULADO": return 306
    elif estado == "PENDIENTE/DVTO. EN CIA": return 216

def get_carpeta_grupo(codigo):
    if codigo == 1: return "CLIENTES".lower()
    elif codigo == 6: return "ASEGURADORAS".lower()
    elif codigo == 0: return "GENERAL".lower()
    elif codigo == 3: return "POLIZAS".lower()
    elif codigo == 14: return "PROYECTOS".lower()
    elif codigo == 4: return "RECIBOS".lower()
    elif codigo == 5: return "SINIESTROS".lower()

def get_uso_auto(codigo):
    list = [
        (1, 1), # 1 : "PARTICULAR" 1
        (2, 18), # 2 : "PLAR/TTES PROPIOS" 18
        (3, 0), # 3 : "TTES.PROPIOS"
        (4, 0), # 4 : "TTES.PROPIOS TIR"
        (5, 7), # 5 : "ALQUILER SIN COND." 7
        (6, 7), # 6 : "ALQUILER CON COND." 7
        (7, 4), # 7 : "S.P.SIN TAXIMETRO" 4
        (8, 4), # 8 : "S.P.CON TAX.C.PRO" 4
        (9, 4), # 9 : "S.P.CON TAX.C.EMP" 4
        (10, 2), # 10 : "S.P." 2
        (11, 2), # 11 : "S.P.> 300" 2
        (12, 2), # 12 : "S.P.< 300 TIR"  2
        (13, 2), # 13 : "S.P.< 300" 2
        (14, 2), # 14 : "S.P.> 300 TIR" 2
        (15, 0), # 15 : "VEHICULO COLECCION"
        (16, 0), # 16 : "AMBULANCIA"
        (17, 8), # 17 : "AUTOESCUELA" 8
        (18, 0), # 18 : "DISCRECIONAL"
        (19, 0), # 19 : "LINEA REGULAR"
        (20, 0), # 20 : "URBANO" 0
        (21, 0), # 21 : "POLICIA " 0
        (22, 0), # 22 : "CAMION BASURA " 0
    ]

    if codigo is None or not 1 >= int(codigo) <= len(list):
        return 0
    else:
        return list[codigo-1][1]        

def get_cia_pacc(registro):
    if registro == []:
        return 0

    codigo = registro["cia_poliza"]
    if codigo is None:
        return 0
        
    codigo = int(codigo)

    if codigo == 19: return 22; #"nombre_cia" : "ASISA, ASISTENCIA SANITARIA INTERPROVINCIAL DE SEGUROS, S.A." ,
    elif codigo == 24: return 7; # "SANTA LUCIA, S.A. COMPA??IA DE SEGUROS Y REASEGUROS" , "cia_abre
    elif codigo == 25: return 198; # "AXA PENSIONES S.A ENT.GEST.DE FONDOS" , "cia_abreviatura" : "AX
    elif codigo == 12: return 14; # "OCASO, S.A., COMPA??IA DE SEGUROS Y REASEGUROS." , "cia_abreviat
    elif codigo == 20: return 0; # "MUTUAL DE CONDUCTORS, MUTUALIDAD DE PREVISION SOCIAL A PRIMA FI
    elif codigo == 21: return 0; # "SVRNE, MUTUA DE SEGUROS Y REASEGUROS A PRIMA FIJA" , "cia_abrev
    elif codigo == 18: return 42; # "SANTA LUCIA VIDA Y PENSIONES S.A" , "cia_abreviatura" : "SANTA 
    elif codigo == 8 : return 1; #"PLUS ULTRA SEGUROS GENERALES Y VIDA, S.A. DE SEGUROS Y REASEGURO
    elif codigo == 2 : return 33; #"ARAG SE SUC.ESPA??A" , "cia_abreviatura" : "ARAG" , "cod_interno_
    elif codigo == 1 : return 13; #"ALLIANZ, COMPA??IA DE SEGUROS Y REASEGUROS, SOCIEDAD ANONIMA" , "
    elif codigo == 22: return 0; # "W.R. BERKLEY EUROPE AG SUC. ESPA??A" , "cia_abreviatura" : "BERK
    elif codigo == 16: return 43; # "L'EQUITE - XENASEGUR " , "cia_abreviatura" : "XENASEGUR" , "cod
    elif codigo == 26: return 58; # "MAPFRE VIDA, S.A. DE SEGUROS Y REASEGUROS SOBRE LA VIDA HUMANA"
    elif codigo == 14: return 26; # "SANITAS, SOCIEDAD ANONIMA DE SEGUROS." , "cia_abreviatura" : "S
    elif codigo == 27: return 20; # "W.R. BERKLEY EUROPE AG SUC. ESPA??A" , "cia_abreviatura" : "BERK
    elif codigo == 5 : return 4; #"DKV SEGUROS Y REASEGUROS, SOCIEDAD ANONIMA ESPA??OLA" , "cia_abre
    elif codigo == 11: return 38; # "REALE SEGUROS GENERALES, S.A." , "cia_abreviatura" : "REALE" , 
    elif codigo == 17: return 53; # "AEGON ESPA??A, SOCIEDAD AN??NIMA DE SEGUROS Y REASEGUROS" , "cia_
    elif codigo == 23: return 21; # "AXA AURORA VIDA, S.A. DE SEGUROS Y REASEGUROS" , "cia_abreviatu
    elif codigo == 13: return 9; # "ZURICH INSURANCE PLC SUC.ESPA??A" , "cia_abreviatura" : "ZURICH"
    elif codigo == 4 : return 2; #"AXA SEGUROS GENERALES, S. A. DE SEGUROS Y REASEGUROS" , "cia_abr
    elif codigo == 9 : return 34; #"LIBERTY SEGUROS, COMPA??IA DE SEGUROS Y REASEGUROS, S.A." , "cia_
    elif codigo == 7 : return 8; #"GENERALI ESPA??A, SOCIEDAD AN??NIMA DE SEGUROS Y REASEGUROS" , "ci
    elif codigo == 10: return 27; # "MAPFRE FAMILIAR, COMPA??IA DE SEGUROS Y REASEGUROS, S.A." , "cia
    elif codigo == 6 : return 49; #"FIATC, MUTUA DE SEGUROS Y REASEGUROS A PRIMA FIJA" , "cia_abrevi
    elif codigo == 3 : return 46; #"ASEFA, S.A. COMPA????A ESPA??OLA DE SEGUROS Y REASEGUROS" , "cia_ab
    else: return 0

# Fn equivalencia ramos pacc
def get_ramo_pacc(registro):
    if registro == []:
        return 0

    codigo = registro["producto"]
    if codigo is None:
        return 0

    if codigo == '21703': return 604 # S.O.ACT.NAUTICAS
    elif codigo == '20901': return 302 # GASTOS REEMBOL.
    elif codigo == '20902': return 305 # GASTOS CONCERT.
    elif codigo == '20903': return 305 # MIXTO REEM-CON.
    elif codigo == '20701': return 101 # ACC.INDIVIDUAL
    elif codigo == '20702': return 701 # ACC.COLECTIVOS
    elif codigo == '20703': return 700 # ACC.CONV.LABOR.
    elif codigo == '20704': return 101 # ACC.OCUP.AUTOS
    elif codigo == '20806': return 207 # AGRICOLA
    elif codigo == '21601': return 000 # GANADO
    elif codigo == '21602': return 000 # ACUICOLAS
    elif codigo == '21603': return 000 # FORESTALES
    elif codigo == '21604': return 000 # CUL.HER.EXTENSIVOS
    elif codigo == '21605': return 000 # FRUTALES
    elif codigo == '21606': return 000 # CITRICOS
    elif codigo == '21607': return 000 # PLATANO
    elif codigo == '21608': return 000 # FRUTOS SECOS
    elif codigo == '21609': return 000 # HORTALIZAS
    elif codigo == '21610': return 000 # CUL.PROTEGIDOS
    elif codigo == '21611': return 000 # PATATA
    elif codigo == '21612': return 000 # CUL.INDUSTRIALES
    elif codigo == '21613': return 000 # OLIVAR
    elif codigo == '21614': return 000 # VI?????EDO
    elif codigo == '21615': return 000 # TARIFA GENERAL
    elif codigo == '21616': return 000 # M.E.R.
    elif codigo == '21617': return 000 # FRUTOS TROPICALES
    elif codigo == '21201': return 212 # ASIVIA PERSONAS
    elif codigo == '21202': return 220 # ASIVIA AUTOS
    elif codigo == '10101': return 614 # TURISMOS/FURGO.
    elif codigo == '10103': return 615 # FURGONETA >700K
    elif codigo == '10104': return 614 # CUADRICICLO
    elif codigo == '10201': return 601 # CAMION RIGIDO
    elif codigo == '10202': return 601 # CABEZA TRACTORA
    elif codigo == '10203': return 601 # REMOLQUE
    elif codigo == '10204': return 618 # VEH.ESPECIAL
    elif codigo == '10205': return 609 # AUTOBUS
    elif codigo == '10301': return 617 # MOTOCICLETA
    elif codigo == '10302': return 617 # CICLOMOTOR
    elif codigo == '10303': return 614 # CUADRICICLO
    elif codigo == '10304': return 617 # QUADS
    elif codigo == '20603': return 126 # AVER.MAQUINARIA
    elif codigo == '21501': return 800 # CAUCION
    elif codigo == '20803': return 209 # COMERCIOS
    elif codigo == '20802': return 203 # COMUNIDADES
    elif codigo == '21401': return 802 # CREDITO
    elif codigo == '21701': return 119 # CRISTALES
    elif codigo == '20420': return 127 # CYBERRIESGOS
    elif codigo == '20605': return 117 # S.O.DECENAL DA?????OS
    elif codigo == '21001': return 421 # DECESOS
    elif codigo == '21801': return 408 # DEPENDENCIA
    elif codigo == '20604': return 110 # EQUI.ELECTRONI.
    elif codigo == '20801': return 201 # HOGAR
    elif codigo == '20807': return 206 # HOTELES
    elif codigo == '21704': return 221 # IMP.ALQUILERES
    elif codigo == '20101': return 000 # INC.RIES.SENCI.
    elif codigo == '20102': return 000 # INC.RIES.INDUS.
    elif codigo == '21705': return 300 # MASCOTAS
    elif codigo == '20804': return 204 # OFICINAS
    elif codigo == '21702': return 212 # OTROS RAMOS
    elif codigo == '20201': return 105 # PER.BENEFICIOS
    elif codigo == '20202': return 104 # SUS.ESPECTACUL.
    elif codigo == '21101': return 222 # P.J.AUTOS
    elif codigo == '21102': return 222 # P.J.GENERAL
    elif codigo == '20805': return 206 # P.Y.M.E.
    elif codigo == '20401': return 103 # R.C.GENERAL
    elif codigo == '20402': return 115 # R.C.PROFESIONAL
    elif codigo == '20403': return 103 # R.C.P.NUCLEAR
    elif codigo == '20404': return 108 # R.C.CAZA OBLIG.
    elif codigo == '20405': return 108 # R.C.CAZA VOLUN.
    elif codigo == '20406': return 103 # R.C.DECENAL
    elif codigo == '20407': return 103 # R.C.EMPRESAS
    elif codigo == '20408': return 102 # R.C.CONSEJEROS
    elif codigo == '20409': return 509 # R.C.EMBARCA.OBLIG.
    elif codigo == '20410': return 108 # R.C.PESCA OBLIG.
    elif codigo == '20411': return 114 # R.C.AGRARIA
    elif codigo == '20412': return 103 # R.C.DRON OBLIG.
    elif codigo == '20413': return 118 # R.C.MEDIOAMBIENTAL
    elif codigo == '20501': return 111 # ROBO
    elif codigo == '20706': return 604 # S.O.VIAJEROS
    elif codigo == '20705': return 304 # SUB.ENF.ACCID.
    elif codigo == '21301': return 000 # SURECA
    elif codigo == '20103': return 210 # T.R.DA?????OS
    elif codigo == '20808': return 210 # TODO RIESGO INDUSTRIAL
    elif codigo == '20601': return 109 # T.R.CONSTRUCCI.
    elif codigo == '20602': return 109 # T.R.MONTAJE
    elif codigo == '20301': return 500 # MERCA.TERRESTR.
    elif codigo == '20302': return 500 # MERCA.MARITIMO
    elif codigo == '20303': return 500 # MERCA.AEREO
    elif codigo == '20304': return 500 # MERCA.MIXTO
    elif codigo == '20305': return 503 # CASCOS NAVEGAC.
    elif codigo == '20306': return 503 # CASCOS CONSTRU.
    elif codigo == '20307': return 000 # R.L.REPARADORES
    elif codigo == '20308': return 509 # EMBARCA.RECREO
    elif codigo == '20309': return 211 # CARAVANAS
    elif codigo == '20310': return 502 # AERONAVES
    elif codigo == '20311': return 503 # CASCOS P&I
    elif codigo == '30108': return 422 # UNILINK
    elif codigo == '30211': return 423 # UNILINK
    elif codigo == '30101': return 415 # IND.DIFE.AHORRO
    elif codigo == '30102': return 400 # IND.RIESGO
    elif codigo == '30103': return 400 # IND.MIXTOS
    elif codigo == '30104': return 702 # COL.DIFE.AHORRO
    elif codigo == '30105': return 702 # COL.RIESGO
    elif codigo == '30106': return 000 # COL.MIXTOS
    elif codigo == '30107': return 428 # FOND.PENSIONES
    elif codigo == '30109': return 406 # PPA
    elif codigo == '30110': return 432 # FOND.PENSIONES RFCP
    elif codigo == '30111': return 432 # FOND.PENSIONES RFLP
    elif codigo == '30112': return 432 # FOND.PENSIONES RFMI
    elif codigo == '30113': return 432 # FOND.PENSIONES RVMI
    elif codigo == '30114': return 432 # FOND.PENSIONES RVAR
    elif codigo == '30115': return 432 # FOND.PENSIONES GARA
    elif codigo == '30116': return 433 # SIALP
    elif codigo == '30117': return 415 # PIAS
    elif codigo == '30118': return 000 # EPSV
    elif codigo == '30201': return 000 # COL.AHORRO
    elif codigo == '30202': return 000 # COL.RIESGO
    elif codigo == '30203': return 000 # COL.MIXTOS
    elif codigo == '30204': return 417 # IND.AHORRO
    elif codigo == '30205': return 400 # IND.RIESGO
    elif codigo == '30206': return 000 # IND.MIXTOS
    elif codigo == '30207': return 425 # RENTA VITALICIA
    elif codigo == '30208': return 432 # FOND.PENSIONES
    elif codigo == '30209': return 400 # P.FINANCIEROS
    elif codigo == '30210': return 425 # RENTAS TEMPORALES
    elif codigo == '30212': return 406 # PPA
    elif codigo == '30213': return 432 # FOND.PENSIONES RFCP
    elif codigo == '30214': return 432 # FOND.PENSIONES RFLP
    elif codigo == '30215': return 432 # FOND.PENSIONES RFMI
    elif codigo == '30216': return 432 # FOND.PENSIONES RVMI
    elif codigo == '30217': return 432 # FOND.PENSIONES RVAR
    elif codigo == '30218': return 432 # FOND.PENSIONES GARA
    elif codigo == '30219': return 433 # SIALP
    elif codigo == '30220': return 415 # PIAS
    elif codigo == '30221': return 000 # EPSV
    elif codigo == '05001': return 305
    else: return 000

def importFile(name):
    path_files = config('database.ini','setting')["path_files"]
    list = []

    with open(f'{path_files}/eb_{name}.txt', encoding="utf8") as f:
        for jsonObj in f:
            resourceDict = json.loads(jsonObj)
            list.append(resourceDict)

    # prRed('\n-------\n'+name+'\n-------')
    # print('\n'.join((resourceDict.keys())))
    return list    
       
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
 
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
 
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))

#########################

