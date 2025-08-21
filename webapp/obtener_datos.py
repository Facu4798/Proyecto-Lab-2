def obtener_datos(query, user, host, password, port, database):
    """
    Esta función se conecta a una base de datos PostgreSQL y ejecuta una consulta SQL.
    Devuelve el resultado de la consulta como un DataFrame de pandas.
    """
    #import pandas
    try:
        import pandas as pd
    except ImportError:
        import os
        os.system('pip install pandas')
        import pandas as pd
    
    #import mysql connector
    try:
        import mysql.connector
    except ImportError:
        import os
        os.system('pip install mysql-connector-python')
        import mysql.connector

    # Crear la conexión a la base de datos
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )
    # Crear un cursor para ejecutar la consulta
    cursor = connection.cursor()
    # Ejecutar la consulta
    cursor.execute(query)
    # Obtener los resultados
    results = cursor.fetchall()
    # Obtener los nombres de las columnas
    column_names = [i[0] for i in cursor.description]

    return pd.DataFrame(results, columns=column_names).set_index('Date')