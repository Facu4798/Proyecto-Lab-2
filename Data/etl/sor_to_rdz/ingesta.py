

from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from la_libreria.utils import get_ts

def obtener_datos(inicio=None, fin=None, ticker='TSLA',credentials=None):
    import io
    import requests
    import ftplib

    #importar pandas
    try:
        import pandas as pd
    except:
        import os
        os.system('pip install pandas')
        import pandas as pd

    #validacion de fecha
    if inicio is None or fin is None:
        pass
    elif not isinstance(inicio, str) or not isinstance(fin, str):
        raise ValueError("Las fechas deben ser cadenas en formato 'YYYY-MM-DD'")
    elif inicio >= fin:
        raise ValueError("La fecha de inicio debe ser menor que la fecha de fin")
    
    etl_ts = get_ts()



    #ingestar los datos de yahoo finance
    from ingesta_yahoo import obtener_datos_yahoo
    data_yahoo = obtener_datos_yahoo(
        ticker=ticker,
        start=inicio,
        end=fin,
    )
    data_yahoo["Ticker"]=ticker
    data_yahoo = data_yahoo.reset_index()
    data_yahoo = data_yahoo.rename(columns={"index":"Date"})
    data_yahoo = data_yahoo[["Date","Ticker","Open","High","Low","Close","Volume"]]
    data_yahoo["etl_ts"] = etl_ts

    #ingestar los datos de FRED
    from ingesta_fred import obtener_datos_fred
    data_fred = obtener_datos_fred(
        start=inicio,
        end=fin
        )
    data_fred = [df.reset_index() for df in data_fred]
    data_fred = [df.rename(columns={"index":"Date"}) for df in data_fred]
    for df in data_fred:
        df["Series"] = df.columns[1]
    data_fred = [df.rename(columns={df.columns[1]:"Value"}) for df in data_fred]
    data_fred = pd.concat(data_fred,axis=0)
    data_fred["etl_ts"] = etl_ts

    conn = MySQLConnector(credentials.dict)
    conn.test_connection()
    conn.connect()

    try:
        conn.create_table(
            data=data_yahoo,
            table_name="stock_data",
            pks=["Date","Ticker"],
            exceptions={"Volume":"BIGINT"}
        )
    except:
        pass

    try:
        conn.create_table(
            data=data_fred,
            table_name="macro_data",
            pks=["Date","Series"],
            exceptions={}
        )
    except:
        pass

    conn.insert_data(
        data=data_yahoo,
        table_name="stock_data",
        pks=["Date","Ticker"]
    )
    
    conn.insert_data(
        data = data_fred,
        table_name="macro_data",
        pks=["Date","Series"]
    )

    conn.insert_data(
        pd.DataFrame({"date":[etl_ts],"description":[f"sor_to_rdz {ticker}"]}),
        table_name="cdc",
        pks=["description"]
    )

    conn.close()



creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_prod.json")

from cdc import get_cdc_date
cdc_date = get_cdc_date("sor_to_rdz ^GSPC")
if cdc_date is not None:
    from la_libreria.utils import substract_date
    cdc_date = substract_date(str(cdc_date),interval="d",amount=1)
try:
    obtener_datos(
        inicio=cdc_date,
        fin=None, 
        ticker='^GSPC',
        credentials = creds
    )
except Exception as e:
    print("Error al obtener datos de ^GSPC:", e)
