from la_libreria.authentication import Credentials
creds = Credentials().load(path="Credentials/db_prod.json")
from la_libreria.connectors import MySQLConnector

conn = MySQLConnector(creds.dict)
conn.connect()
data=conn.get_data("SELECT * FROM macro_data")
# print(data.tail())

import yfinance as yf
data = yf.download("^GSPC")
print(len(data))