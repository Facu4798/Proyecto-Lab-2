import sys
from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from obtener_datos import obtener_datos
from cargar_datos import cargar_datos
from cdc import get_cdc_date


shift = 35
cdc_date = get_cdc_date("rdz_to_cdz")
ticker="^GSPC"


try:
    creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_prod.json")
except: 
    sys.exit("Credentials file not found")



try:
    q = open("/workspaces/Proyecto-Lab-2/Data/etl/rdz_to_cdz/union.sql","r").readlines()
    q = "".join([l.replace("\n","") for l in q ])
    if cdc_date is None:
        q = q.replace("Date >= date_placeholder","1=1")
    else:
        q = q.replace("ticker_placeholder", ticker)
    q = q.replace("date_placeholder", str(cdc_date))
except:
    sys.exit("query file not found")


try:
    conn = MySQLConnector()
    conn.connect(creds.dict)
    data = conn.get_data(query=q)
except Exception as e:
    sys.exit(e)


try:
    conn.insert_data(data,table_name="curated",pks=["Date","Ticker"])
    conn.close()
except Exception as e:
    sys.exit(e)
