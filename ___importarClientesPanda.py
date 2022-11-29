
import pandas as pd
from datetime import datetime
def dateparse(x): return datetime.strptime(x, '%d/%m/%Y')


rows = pd.read_json('datos/eb_clientes.txt', lines=True,
orient='records'
    # sep=';',
    # usecols=['POLIZA', 'NOM TOMADOR',
    #         'RIESGO', 'FH VENCIMIENTO'],
    # parse_dates=['FH VENCIMIENTO'],
    # date_parser=dateparse
    )

print(rows)
# print(rows.to_string())                    

# show first 5 lines
# print(rows.head())

# print(rows.shape)
# print(rows.info())