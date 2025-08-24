

from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from la_libreria.utils import get_ts

def cargar_datos_fred(inicio=None, fin=None, credentials=None):
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
            data=data_fred,
            table_name="macro_data",
            pks=["Date","Series"],
            exceptions={}
        )
    except:
        pass
    
    conn.insert_data(
        data = data_fred,
        table_name="macro_data",
        pks=["Date","Series"]
    )

    last_date = data_fred.groupby("Series").agg({"Date":"max"})['Date'].min().strftime("%Y-%m-%d")
    conn.insert_data(
        pd.DataFrame({"date":[last_date],"description":[f"sor_to_rdz fred"]}),
        table_name="cdc",
        pks=["description"]
    )

    conn.close()

