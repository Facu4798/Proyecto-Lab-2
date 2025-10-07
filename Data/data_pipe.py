import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = current_dir.rsplit('Proyecto-Lab-2', 1)[0] + 'Proyecto-Lab-2/'
os.chdir(current_dir)
print(current_dir)

sys.path.insert(0, current_dir)

#generar la conexion a la base de datos
from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_dev.json")
conn = MySQLConnector(creds.dict).connect()

# ejecutar los procesos ETL
from Data.etl.sor_to_rdz.ingesta import ingestar
from Data.etl.rdz_to_cdz.curado import curar

ingestar(conn=conn,creds=creds)
curar(conn=conn,creds=creds)

sys.path.pop(0)

conn.close()