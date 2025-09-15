from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from la_libreria.utils import get_ts


def monitor_table(date,
                    ticker,
                    p5,
                    p10,
                    p30):

    import pandas as pd

    credentials = Credentials().load(path="Credentials/db_prod.json")
    conn = MySQLConnector(credentials.dict)
    conn.test_connection()
    conn.connect()

    monitoreo_table = pd.DataFrame({
                                        "date": [date],
                                        "Ticker": [ticker],
                                        "p5": [p5],
                                        "p10": [p10],
                                        "p30": [p30],
                                        "r5": [None],
                                        "r10": [None],
                                        "r30": [None],
                                        "Comparacion_5": [False],
                                        "Comparacion_10": [False],
                                        "Comparacion_30": [False]
                                    }
                                   )
    
    try:
        conn.create_table(
            data=monitoreo_table,
            table_name="monitoreo",
            pks=["date"],
            exceptions={}
        )
    except Exception:
        print("La tabla ya existe")
        pass

    conn.insert_data(
        data=monitoreo_table,
        table_name="monitoreo",
        pks=["date"]
    )

    conn.close()



def cargar_data_real(r5, date5, r10, date10, r30, date30):
    
    import pandas as pd
    credentials = Credentials().load(path="Credentials/db_prod.json")
    conn = MySQLConnector(credentials.dict)
    conn.test_connection()
    conn.connect()

    monitor_fila_5 = conn.get_data(f"SELECT * FROM monitoreo WHERE date = '{date5}'")
    if not monitor_fila_5.empty:
        monitor_fila_5['r5'] = r5
        monitor_fila_5['Comparacion_5'] = True

    conn.insert_data(
        data=monitor_fila_5,
        table_name="monitoreo",
        pks=["date"]
    )

    monitor_fila_10 = conn.get_data(f"SELECT * FROM monitoreo WHERE date = '{date10}'")
    if not monitor_fila_10.empty:
        monitor_fila_10['r10'] = r10
        monitor_fila_10['Comparacion_10'] = True

    conn.insert_data(
        data=monitor_fila_10,
        table_name="monitoreo",
        pks=["date"]
    )

    monitor_fila_30 = conn.get_data(f"SELECT * FROM monitoreo WHERE date = '{date30}'")
    if not monitor_fila_30.empty:
        monitor_fila_30['r30'] = r30
        monitor_fila_30['Comparacion_30'] = True

    conn.insert_data(
        data=monitor_fila_30,
        table_name="monitoreo",
        pks=["date"]
    )
    
    conn.close()
    