from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from la_libreria.utils import get_ts
import os
from la_libreria.utils import parse_query
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv("moni.env"))
# os.system("clear")
import pandas as pd

def metric_monitoring():

    credentials = Credentials().load(path=os.getenv("DEV_CREDS"))
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
        metric = conn.get_data(parse_query(
            filepath=os.getenv("MODEL_TRACKING_SQL"),
            replacement_dict={"ticker_placeholder": Ticker, "t_placeholder": t}
        ))
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
        

    conn.close()