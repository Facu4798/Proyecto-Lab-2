from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
import os
os.system("clear")
creds = Credentials().load(path="Credentials/db_dev.json")
conn = MySQLConnector(creds.dict)
conn.connect()
print(conn.get_data(query="select * from cdc"))
conn.close()

# import pandas as pd

# data = pd.DataFrame({
#     "Date": ["2023-01-01","2023-01-02","2023-01-03"],
#     "Ticker": ["^GSPC","^GSPC","^GSPC"]
# })

# print(str(data.iloc[-1]["Date"]))