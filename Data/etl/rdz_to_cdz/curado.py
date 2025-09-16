import sys
import os
import pandas as pd
from la_libreria.utils import substract_date,get_ts
from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from cdc import get_cdc_date
os.system("clear")

# parametros de la corrida
shift = 35
cdc_date = get_cdc_date("rdz_to_cdz")
if cdc_date is not None:
    cdc_date = substract_date(date_str=str(cdc_date),
                              amount=shift,
                              iterval="d")
ticker="^GSPC"

# leer las credenciales de la base de datos
try:
    creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_dev.json")
except: 
    sys.exit("Credentials file not found")


# leer el archivo de la query
try:
    q = open("/workspaces/Proyecto-Lab-2/Data/etl/rdz_to_cdz/union copy.sql","r").readlines()
    q = "".join([l.replace("\n"," ") for l in q ])
    if cdc_date is None:
        q = q.replace("Date >= 'date_placeholder'","1=1")
    else:
        q = q.replace("date_placeholder",str(cdc_date))
    q = q.replace("ticker_placeholder", ticker)
    q = q.replace(";","")
    
except:
    sys.exit("query file not found")

# obtener los datos de rdz
try:
    conn = MySQLConnector(creds.dict)
    conn.connect()
    data = conn.get_data(query=q)
    data["etl_ts"] = str(get_ts())
    conn.close()
except Exception as e:
    sys.exit(e)


# intentar crear la tabla curated
try:
    conn = MySQLConnector(creds.dict)
    conn.connect()
    conn.create_table(data=data,table_name="curated",pks=["Date","Ticker"])
    conn.close()
except Exception as e:
    print(e)


# guardar los datos en cdz y el watermark
try:
    conn = MySQLConnector(creds.dict)
    conn.connect()
    conn.insert_data(data=data,table_name="curated",pks=["Date","Ticker"])
    last_date = str(data.iloc[-1]["Date"])
    conn.insert_data(data=pd.DataFrame(
        {
            "description":["rdz_to_cdz"],
            "date":[last_date]
        }),
        table_name="cdc",pks=["description"]
    )
    conn.close()
except Exception as e:
    sys.exit(e)




