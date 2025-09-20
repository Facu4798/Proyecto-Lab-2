from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector

creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_prod.json")
conn = MySQLConnector(creds.dict)
conn.connect()
data = conn.get_data("select * from predicciones")
conn.close()
print(data)