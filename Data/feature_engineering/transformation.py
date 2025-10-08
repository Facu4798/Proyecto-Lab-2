from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from la_libreria.utils import parse_query
from la_libreria.utils import substract_date
from cdc_l3 import get_cdc_date
import sys
import pandas as pd
import os
os.system('clear')

creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_dev.json")
conn = MySQLConnector(creds.dict)
conn.connect()

ticker="^GSPC"
drop=False
reset_date=False

if reset_date:
    conn.cursor.execute(f"DELETE FROM cdc WHERE Description='cdz_to_ddz {ticker}';")
    conn.connection.commit()

cdc_date = get_cdc_date(f"cdz_to_ddz {ticker}",creds=creds)

if cdc_date is not None:
    cdc_date = substract_date(str(cdc_date), interval="d",amount=1000)
    cdc_date = f"Date >= '{cdc_date}'"
else:
    cdc_date = "1=1"

query_file = "/workspaces/Proyecto-Lab-2/Data/feature_engineering/train_data.sql"

query = parse_query(query_file, replacement_dict={"Date >= date_placeholder": cdc_date,
                                                        "limit_placeholder": "400",
                                                        "ticker_placeholder": ticker})

# obtener datos de cdz
try:
    data = conn.get_data(query).drop(columns=["etl_ts"])
except Exception as e:
    sys.exit("ERROR: " + str(e))

print(data.shape[0])
#transformar datos
try:
    from transformar_datos import transformar_datos
    data,columns_to_drop = transformar_datos(data)
    print("transformed data")
except Exception as e:
    sys.exit("ERROR: " + str(e))




if drop:
    try:
        conn.cursor.execute(f"DROP TABLE IF EXISTS delivery;")
        conn.connection.commit()
        print("dropped table")
    except Exception as e:
        sys.exit(e)


# crear tabla si no existe
try:
    conn.create_table(data=data,
                      table_name="delivery",
                      pks=["Date","Ticker"],
                      exceptions={"Volume":"BIGINT"})
except Exception as e:
    sys.exit("ERROR"+e)

# insertar datos en la tabla
try:
    conn.insert_data(data=data,
                     table_name="delivery",
                     pks=["Date","Ticker"])
except Exception as e:
    sys.exit(e)

# guardar el watermark en la tabla de cdc
try:
    conn.insert_data(data=pd.DataFrame(
        {
            "Description": [f"cdz_to_ddz {ticker}"],
            "Date": [str(pd.to_datetime("now"))]
        }
    ),table_name="cdc",pks=["Description"])
except Exception as e:
    sys.exit(e)