from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector

creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_dev.json")
conn = MySQLConnector(creds.dict)
conn.connect()
print(conn.get_data("""Select table_name,column_name from information_schema.columns where
table_name='curated' """))
conn.close()