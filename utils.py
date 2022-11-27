from datetime import datetime

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
        return numero
    elif not es_numero_movil and not campo_movil:
        return numero
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
    
    if valor == 'C':
        return 'CAS'
    elif valor == 'V':
        return 'VID'
    elif valor == 'D':
        return 'DIV'
    elif valor == 'S':
        return 'SOL' 
    elif valor == 'S':
        return 'SEP'
    else:
        return ''    

def getSituacion(valor):
    if valor is None:
        return 0
    if valor == "ANULADA":
        return 5
    else:
        return 1

def getMotivoAnulacion(valor):
    if valor == "ANULADA":
        return 7
    else:
        return 0    

def getCodCia(codigo):
    if codigo is None:
        return 0
        
    codigo = int(codigo)

    if codigo == 19: 
        return 22; #"nombre_cia" : "ASISA, ASISTENCIA SANITARIA INTERPROVINCIAL DE SEGUROS, S.A." ,
    elif codigo == 24: 
        return 7; # "SANTA LUCIA, S.A. COMPAÑIA DE SEGUROS Y REASEGUROS" , "cia_abre
    elif codigo == 25: 
        return 198; # "AXA PENSIONES S.A ENT.GEST.DE FONDOS" , "cia_abreviatura" : "AX
    elif codigo == 12: 
        return 14; # "OCASO, S.A., COMPAÑIA DE SEGUROS Y REASEGUROS." , "cia_abreviat
    elif codigo == 20: 
        return 0; # "MUTUAL DE CONDUCTORS, MUTUALIDAD DE PREVISION SOCIAL A PRIMA FI
    elif codigo == 21: 
        return 0; # "SVRNE, MUTUA DE SEGUROS Y REASEGUROS A PRIMA FIJA" , "cia_abrev
    elif codigo == 18: 
        return 42; # "SANTA LUCIA VIDA Y PENSIONES S.A" , "cia_abreviatura" : "SANTA 
    elif codigo == 8 : 
        return 1; #"PLUS ULTRA SEGUROS GENERALES Y VIDA, S.A. DE SEGUROS Y REASEGURO
    elif codigo == 2 : 
        return 33; #"ARAG SE SUC.ESPAÐA" , "cia_abreviatura" : "ARAG" , "cod_interno_
    elif codigo == 1 : 
        return 13; #"ALLIANZ, COMPAÑIA DE SEGUROS Y REASEGUROS, SOCIEDAD ANONIMA" , "
    elif codigo == 22: 
        return 0; # "W.R. BERKLEY EUROPE AG SUC. ESPAÑA" , "cia_abreviatura" : "BERK
    elif codigo == 16: 
        return 0; # "L'EQUITE - XENASEGUR " , "cia_abreviatura" : "XENASEGUR" , "cod
    elif codigo == 26: 
        return 58; # "MAPFRE VIDA, S.A. DE SEGUROS Y REASEGUROS SOBRE LA VIDA HUMANA"
    elif codigo == 14: 
        return 26; # "SANITAS, SOCIEDAD ANONIMA DE SEGUROS." , "cia_abreviatura" : "S
    elif codigo == 27: 
        return 0; # "W.R. BERKLEY EUROPE AG SUC. ESPAÑA" , "cia_abreviatura" : "BERK
    elif codigo == 5 : 
        return 4; #"DKV SEGUROS Y REASEGUROS, SOCIEDAD ANONIMA ESPAÑOLA" , "cia_abre
    elif codigo == 11: 
        return 38; # "REALE SEGUROS GENERALES, S.A." , "cia_abreviatura" : "REALE" , 
    elif codigo == 17: 
        return 53; # "AEGON ESPAÐA, SOCIEDAD ANËNIMA DE SEGUROS Y REASEGUROS" , "cia_
    elif codigo == 23: 
        return 21; # "AXA AURORA VIDA, S.A. DE SEGUROS Y REASEGUROS" , "cia_abreviatu
    elif codigo == 13: 
        return 9; # "ZURICH INSURANCE PLC SUC.ESPAÑA" , "cia_abreviatura" : "ZURICH"
    elif codigo == 4 : 
        return 2; #"AXA SEGUROS GENERALES, S. A. DE SEGUROS Y REASEGUROS" , "cia_abr
    elif codigo == 9 : 
        return 34; #"LIBERTY SEGUROS, COMPAÑIA DE SEGUROS Y REASEGUROS, S.A." , "cia_
    elif codigo == 7 : 
        return 8; #"GENERALI ESPAÑA, SOCIEDAD ANÓNIMA DE SEGUROS Y REASEGUROS" , "ci
    elif codigo == 10: 
        return 27; # "MAPFRE FAMILIAR, COMPAÑIA DE SEGUROS Y REASEGUROS, S.A." , "cia
    elif codigo == 6 : 
        return 49; #"FIATC, MUTUA DE SEGUROS Y REASEGUROS A PRIMA FIJA" , "cia_abrevi
    elif codigo == 3 : 
        return 46; #"ASEFA, S.A. COMPAÑÍA ESPAÑOLA DE SEGUROS Y REASEGUROS" , "cia_ab
       
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