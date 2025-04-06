def obtener_de_DL(user='root',
                   password='password',
                   port=3306,
                   host='localhost',
                   start = None,
                   end = None):
    """
    esta función obtiene los datos de la base de datos MySQL
    **Parámetros:**
    - **user:** str, usuario de MySQL (default='root')
    - **password:** str, contraseña de MySQL (default='password')
    - **port:** int, puerto de MySQL (default=3306)
    - **host:** str, host de MySQL (default='localhost')
    - **start:** str, fecha de inicio en formato 'YYYY-MM-DD' (default=None)
    - **end:** str, fecha de fin en formato 'YYYY-MM-DD' (default=None)
    **Retorna:**
    - **data:** diccionario con los datos obtenidos de la base de datos MySQL
    """


    #importar mysql.connector
    try:
        import mysql.connector
        from mysql.connector import Error
    except:
        import os
        os.system('pip install mysql-connector-python')
        import mysql.connector
        from mysql.connector import Error
    #importar pandas
    try:
        import pandas as pd
    except:
        import os
        os.system('pip install pandas')
        import pandas as pd
    
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database='finance_db'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("USE finance_db")

            # Consulta para obtener los datos de la tabla macro_data
            query = "SELECT * from macro_data"

            if start is not None:
                query += f" WHERE date >= '{start}'"
                if end is not None:
                    query += f" AND date <= '{end}'"
            elif end is not None:
                query += f" WHERE date <= '{end}'"
            cursor.execute(query)
            # Obtener todos los resultados
            rows = cursor.fetchall()
            # Obtener los nombres de las columnas
            column_names = [desc[0] for desc in cursor.description]
            # Crear un DataFrame a partir de los resultados
            if len(rows) > 0:
                data_fred = pd.DataFrame(rows, columns=column_names)
                # Convertir la columna 'date' a datetime
                data_fred['date'] = pd.to_datetime(data_fred['date'])
                # Devolver un diccionario con los datos
                return data_fred.set_index('date')
            else:
                print("No se encontraron datos en la tabla macro_data.")
                data_fred = None
            
            query = "SELECT * from stock_data"
            if start is not None:
                query += f" WHERE Date >= '{start}'"
                if end is not None:
                    query += f" AND Date <= '{end}'"
            elif end is not None:
                query += f" WHERE Date <= '{end}'"
            cursor.execute(query)
            # Obtener todos los resultados
            rows = cursor.fetchall()
            # Obtener los nombres de las columnas
            column_names = [desc[0] for desc in cursor.description]
            # Crear un DataFrame a partir de los resultados
            if len(rows) > 0:
                data_stock = pd.DataFrame(rows, columns=column_names)
                # Convertir la columna 'Date' a datetime
                data_stock['Date'] = pd.to_datetime(data_stock['Date'])
                # Devolver un diccionario con los datos
                return data_stock.set_index('Date')
            else:
                print("No se encontraron datos en la tabla stock_data.")
                data_stock = None

    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        data_fred = None
        data_stock = None
    finally:
        # Cerrar la conexión a la base de datos
        if connection.is_connected():
            cursor.close()
            connection.close()
        return {"mcro_data": data_fred, "stock_data": data_stock}