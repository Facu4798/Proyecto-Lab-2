def cargar_datos_fred(data,user='root',
                      password='password',
                     port=3306, 
                     host='localhost',
                     database='defaultdb'):

    """
    Esta función carga los datos de FRED a la base de datos MySQL
    **Parámetros:**
    - **data:** DataFrame, datos a cargar en la base de datos
    - **user:** str, usuario de MySQL (default='root')
    - **password:** str, contraseña de MySQL (default='password')
    - **port:** int, puerto de MySQL (default=3306)
    - **host:** str, host de MySQL (default='localhost')
    """

    #importar mysql connector
    try:
        import mysql.connector
    except:
        import os
        os.system('pip install mysql-connector-python')
        import mysql.connector


    #importar pandas
    try:
        import pandas as pd
    except:
        import os
        os.system('pip install pandas')
        import pandas as pd

    #try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )

    if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"USE {database}")

            # Verificar que la tabla existe, si no crearla
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS macro_data (
                    Date DATE NOT NULL,
                    Value FLOAT,
                    Series VARCHAR(30),
                    PRIMARY KEY (Date, Series)
                )
            """)
            connection.commit()

            for df in data:
                # Cargar los datos en la tabla macro_data
                series = df.columns[0]

                sql_insert = """
                            INSERT INTO macro_data (Date, Value, Series)
                            VALUES (%s, %s, %s)
                            ON DUPLICATE KEY UPDATE 
                            Value = VALUES(Value)
                            """
                
                df["Series"] = series

                df = [
                        tuple(None if pd.isna(value) else value for value in row)
                        for row in df.itertuples(index=True, name=None)
                    ]
                connection.autocommit = True
                cursor.executemany(sql_insert, df)
                connection.commit()


                    
    # except:
    #     print("Error al conectar a la base de datos MySQL")
    #     return None
    
    # finally:
    if connection.is_connected():
        # cerrar cursor y conexión
        try:
            cursor.close()
        except:
            pass
        try:
            connection.close()
        except:
            pass
