#set working directory to current file
import os
import sys
from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from la_libreria.utils import parse_query
from generar_prediccion import generar_prediccion
from model_template import model_template
import pandas as pd
os.system("clear")


#parameters
tickers=["^GSPC"]
days=[5,10,30]
train=True
models_dir = "/workspaces/Proyecto-Lab-2/Models/"
query_path = "/workspaces/Proyecto-Lab-2/src/predictions_and_training/queries/"


M=model_template(
    vol="Garch",
    p=1,
    q=1,
    o=1,
    mean="Zero",
    rescale=True,
    exog_cols=None
)


creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_dev.json")
conn = MySQLConnector(creds.dict)
conn.connect()

# queries to get training or prediction data
queries ={}
for t in tickers:
    for d in days:
        if train:
            q = parse_query(f"{query_path}get_all_{d}_{t}.sql",
                            replacement_dict={"date_placeholder": "1995-01-01"})
            queries[f"{t}_{d}"] = q
        else:
            q = parse_query(f"{query_path}get_last_{d}_{t}.sql",
                            replacement_dict={"limit_placeholder":"400"})
            queries[f"{t}_{d}"] = q


try:
    conn.create_table(
        query= """
        CREATE TABLE predicciones(
            Date DATE,
            Ticker VARCHAR(10),
            5Days FLOAT,
            10Days FLOAT,
            30Days FLOAT,
            PRIMARY KEY(Date,Ticker)
        )
        """
    )
except Exception as e: print(e)


for t in tickers:
    p_temp = []
    for d in days:


        data_temp = conn.get_data(queries[f"{t}_{d}"])
        p = generar_prediccion(modelo=M,
                    models_dir=models_dir,
                    train=train,
                    days=d,
                    data = data_temp,
                    ticker=t)
        p_temp.append(p[1])
    staging_dict = {
        "Date": [p[0]],
        "Ticker": [t],
    }

    for i,d in enumerate(days):
        staging_dict[f"{d}Days"] = [p_temp[i]]
    
    staging_df = pd.DataFrame(staging_dict)
    conn.insert_data(data=staging_df,
                    table_name="predicciones",
                    pks=["Date","Ticker"])
     
        


conn.close()