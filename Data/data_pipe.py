import os
import sys
import time
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv("data.env"))

current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = current_dir.rsplit('Proyecto-Lab-2', 1)[0] + 'Proyecto-Lab-2/'
os.chdir(current_dir)
print(current_dir)

sys.path.insert(0, current_dir)

#generar la conexion a la base de datos
from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector

startup_time = time.time()
creds = Credentials().load(path=os.getenv("DEV_CREDS"))
conn = MySQLConnector(creds.dict).connect()
startup_time = time.time() - startup_time
# ejecutar los procesos ETL
from Data.etl.sor_to_rdz.ingesta import ingestar
from Data.etl.rdz_to_cdz.curado import curar
from Data.feature_engineering.transformation import transformacion

ingest_start = time.time()
ingestar(conn=conn,creds=creds)
ingestion_time = time.time() - ingest_start


curation_start = time.time()
curar(conn=conn,creds=creds)
curation_time = time.time() - curation_start

transformation_start = time.time()
transformacion(conn=conn,creds=creds)
transformation_time = time.time() - transformation_start

os.system("clear")
print(f"Tiempo de inicio y conexion a la base de datos: {startup_time:.2f} segundos.")
print(f"Ingesta completada en {ingestion_time:.2f} segundos.")
print(f"Curado completado en {curation_time:.2f} segundos.")
print(f"Transformacion completada en {transformation_time:.2f} segundos.")
print(f"Tiempo total de ejecucion: {startup_time + ingestion_time + curation_time + transformation_time:.2f} segundos.")

sys.path.pop(0)

conn.close()