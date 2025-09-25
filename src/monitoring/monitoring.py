from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from la_libreria.utils import get_ts
import os
os.system("clear")
import pandas as pd

def metric_monitoring():

    credentials = Credentials().load(path="Credentials/db_prod.json")
    conn = MySQLConnector(credentials.dict)
    conn.test_connection()
    conn.connect()

    Ticker = "^GSPC"
    metric_table = pd.DataFrame({
        "Date": [],
        "MAE": [],
        "Ticker": [],
        "Days": []
    })

    for t in [5,10,30]:
        metric = conn.get_data(f"""                     
        WITH pred_f AS(select * from predicciones where Ticker = '{Ticker}'),
        cur_f AS(select * from curated where Ticker = '{Ticker}'),
        pre AS (
            SELECT c.date as curated_date, 
                p.date as prediction_date,
                c.Target{t} as real_value,
                p.{t}Days prediction,
                c.Ticker 
            FROM cur_f c 
            INNER JOIN pred_f p
            ON c.Date = DATE_ADD(p.Date, INTERVAL {t} DAY)
        )
        SELECT MAX(pre.prediction_date) as Date, 
        AVG(ABS(pre.prediction-pre.real_value)) as MAE,
        '{Ticker}' AS Ticker, 
        '{t}' as Days
        FROM pre
        """)
        metric.dropna(inplace=True)
        if not metric.empty:
            metric_table = pd.concat([metric_table, metric], axis=0)


    try:
        conn.create_table(
            data=metric_table,
            table_name="metric_table",
            pks=["Date", "Ticker", "Days"],
            exceptions={}
        )
    except Exception as e:
        print(e)

    conn.insert_data(
            data=metric_table,
            table_name="metric_table",
            pks=["Date", "Ticker", "Days"]
        )
        

    print(conn.get_data("SELECT * FROM metric_table"))

    conn.close()