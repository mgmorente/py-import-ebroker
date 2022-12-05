# Exportar a fichero
# path_csv = f'{os.path.dirname(__file__)}/__exportacion'
# if not os.path.exists(path_csv):
#     os.makedirs(path_csv, exist_ok=True)

# columnas = '''cod_poliza;poliza;cia_poliza;compania;producto;fecha_efecto;fecha_vencimiento;situacion;nif;nif_asegurado;ase_es_asegurado;matricula;forma_pago;tipo_poliza;objeto;comentario;fecha_alta;fecha_anula;fecha_anula_sis;causa_anula;canal;iban;sucursal;colaborador;created_by\n'''
# with open(f'{path_csv}/polizas.csv', 'w+') as f:
#     f.write(columnas)
#     for items in polizasCodigosList:
#         f.write('%s\n' % items)
# f.close()



# with open(f'{path_csv}/docu-no-existe.csv', 'w+') as f:
#     for items in docuNoExisteList:
#         f.write('%s\n' % items)
# f.close()