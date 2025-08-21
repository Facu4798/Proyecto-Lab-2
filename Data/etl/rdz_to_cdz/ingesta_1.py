

# set working directory to the script's directory
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import sys
# if linux, clear else cls
if sys.platform.startswith('linux'):
    os.system('clear')
else:
    os.system('cls')




def obtener_query(file_path):
    """
    Esta función lee un archivo SQL y devuelve su contenido como una cadena.
    """
    with open(file_path, 'r') as file:
        query = file.read()
    return query



def unir_datos(query,user,host,password,port,database,ticker,start_date):
    query = query.replace("ticker_placeholder", f"'{ticker}'")
    if start_date is None:
        #find where AND src.Date >= start_date_placeholder is in the query
        start_date_index = query.find("AND src.Date >= start_date_placeholder")
        query = query[:start_date_index-1]+";"
    else:
        query = query.replace("start_date_placeholder", f"'{start_date}'")
    
    from obtener_datos import obtener_datos
    df = obtener_datos(query, user, host, password, port, database)


    # Cargar el DataFrame en la base de datos
    from cargar_datos import cargar_datos
    cargar_datos(df, user, password, host, port, database)

    


unir_datos(obtener_query('union.sql'),
            ticker='^GSPC',
            host="estrie01-estimacionderiego1.j.aivencloud.com",
            user="avnadmin",
            password="AVNS_vBt5bLw5TLinvY6G_Eo",
            port=24195,
            database="defaultdb",
            start_date=None)