from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from la_libreria.utils import get_ts


def model_tracking_insert(timestamp,
                          days,
                          nombre_modelo,
                          t_training,
                          n_train,
                          parametros,
                          metrics,
                          last_date,
                          first_date,
                          credentials=None,
                          ticker="^GSPC"):

    import pandas as pd

    credentials = Credentials().load(path="Credentials/db_prod.json")
    conn = MySQLConnector(credentials.dict)
    conn.test_connection()
    conn.connect()

    import json
    # fila por metrica
    rows = []
    for metric_name, metric_value in metrics.items():
        rows.append({
            "Timestamp": timestamp,
            "Days": days,
            "Ticker": ticker,
            "nombre_modelo": nombre_modelo,
            "t_train": t_training,
            "n_train": n_train,
            "parametros": json.dumps(parametros),
            "metric_name": metric_name,
            "metric_value": metric_value,
            "last_date": last_date,
            "first_date": first_date
        })

    model_tracking_table = pd.DataFrame(rows)

    try:
        conn.create_table(
            data=model_tracking_table,
            table_name="model_tracking_table",
            pks=["Timestamp", "Ticker", "Days", "metric_name"],
            exceptions={}
        )
    except Exception:
        pass
    
    conn.get_data("select * from model_tracking")

    conn.insert_data(
        data=model_tracking_table,
        table_name="model_tracking_table",
        pks=["Timestamp", "Ticker", "Days", "metric_name"]
    )
    
    conn.close()
