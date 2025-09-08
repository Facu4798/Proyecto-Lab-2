def obtener_datos(query="",creds=None):
    from la_libreria.connectors import MySQLConnector

    conn = MySQLConnector(creds.dict)
    
    try:
        conn.connect()
    except:
        raise ConnectionError("La conexión a la base de datos falló")
    
    try:
        data = conn.get_data(query=query)
    except:
        raise ValueError("Error al obtener los datos")

    return data