def cargar_datos_fred(data,user='root',
                      password='password',
                     port=3306, 
                     host='localhost',
                     series = "GDP"):

    """
    Esta función carga los datos de FRED a la base de datos MySQL
    **Parámetros:**
    - **data:** DataFrame, datos a cargar en la base de datos
    - **user:** str, usuario de MySQL (default='root')
    - **password:** str, contraseña de MySQL (default='password')
    - **port:** int, puerto de MySQL (default=3306)
    - **host:** str, host de MySQL (default='localhost')
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

                # Verificar que la tabla existe, si no crearla
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS macro_data (
                        date DATE NOT NULL,
                        value FLOAT,
                        series VARCHAR(30)
                        PRIMARY KEY (date)
                    )
                """)
                connection.commit()

                # Cargar los datos en la tabla macro_data
                for index, row in data.iterrows():
                    try:
                        # Insertar cada fila en la tabla
                        cursor.execute("""
                            INSERT INTO macro_data (date, value, series)
                            VALUES (%s, %s, %s)
                            ON DUPLICATE KEY UPDATE value = VALUES(value)
                        """, (index.strftime('%Y-%m-%d'), row[series], series))
                    except Exception as e:
                        print(f"Error al insertar fila {index}: {e}")
                        continue


    except:
        print("Error al conectar a la base de datos MySQL")
        return None
    

    