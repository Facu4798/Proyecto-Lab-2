from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from la_libreria.utils import get_ts


def model_tracking_insert(timestamp,
        target,
        nombre_modelo,
        n_train,
        n_test,
        features,
        parametros,
        metrics,
        last_date,
        first_date,
        ticker,
        training_time,
        prediction_time):

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
            "Target": target,
            "nombre_modelo": nombre_modelo,
            "n_train": n_train,
            "n_test": n_test,
            "features": json.dumps(features),
            "parametros": json.dumps(parametros),
            "metric_name": metric_name,
            "metric_value": metric_value,
            "last_date": last_date,
            "first_date": first_date,
            "Ticker": ticker,
            "training_time": training_time,
            "prediction_time": prediction_time
        })

    model_tracking_table = pd.DataFrame(rows)
    
    try:
        conn.create_table(
            data=model_tracking_table,
            table_name="model_tracking",
            pks=["Timestamp"],
            exceptions={"features":"TEXT", "parametros":"TEXT"}
        )
    except Exception:
        print("La tabla ya existe")
        pass

    conn.insert_data(
        data=model_tracking_table,
        table_name="model_tracking",
        pks=["Timestamp"]
    )
    
    conn.close()
