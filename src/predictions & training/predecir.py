#set working directory to current file
import os
import sys
from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
from la_libreria.utils import parse_query
from generar_prediccion import generar_prediccion
import pandas as pd
os.system("clear")


#parameters
tickers=["^GSPC"]
days=[5,10,30]
train=True
models_dir = "/workspaces/Proyecto-Lab-2/Models/"
query_path = "/workspaces/Proyecto-Lab-2/src/predictions & training/queries/"

from sklearn.linear_model import LinearRegression
M=LinearRegression()


creds = Credentials.load(path="/workspaces/Proyecto-Lab-2/Credentials/db_dev.json")
conn = MySQLConnector(creds.dict)
conn.connect()

# queries to get training or prediction data
queries ={}
for t in tickers:
    for d in days:
        if train:
            q = parse_query(f"{query_path}/get_all_{t}_{t}.sql")
            queries[f"{t}_{d}"] = q
        else:
            q = parse_query(f"{query_path}/get_last_{t}_{t}.sql")
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
        p = generar_prediccion(modelo=M,
                    models_dir=models_dir,
                    train=train,
                    days=d,
                    data = conn.get_data(queries[f"{t}_{d}"]),
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