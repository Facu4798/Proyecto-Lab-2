from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector

creds = Credentials().load(path="Credentials/db_prod.json")

conn = MySQLConnector(creds.dict)
conn.connect()
data = conn.get_data("SELECT * FROM macro_data")
print(data)