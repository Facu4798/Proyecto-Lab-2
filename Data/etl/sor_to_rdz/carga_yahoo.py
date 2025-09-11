def cargar_datos_yahoo(data,
                 user = 'root',
                 password = 'password',
                 port=3306, 
                 host='localhost',
                 ticker='TSLA',
                 database='defaultdb'):
    """
    Esta función carga los datos de yahoo a la base de datos MySQL 
    **Parámetros:**
    - **data:** DataFrame, datos a cargar en la base de datos
    - **user:** str, usuario de MySQL (default='root')
    - **password:** str, contraseña de MySQL (default='password')
    - **port:** int, puerto de MySQL (default=3306)
    - **host:** str, host de MySQL (default='localhost')
    - **ticker:** str, ticker de la acción (default='TSLA')
    """
    try:
        import mysql.connector
        from mysql.connector import Error
    except:
        import os
        os.system('pip install mysql-connector-python')
        import mysql.connector
        from mysql.connector import Error

    try:
        import pandas as pd
    except:
        import os
        os.system('pip install pandas')
        import pandas as pd

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

            # Verificar si la tabla existe, si no, crearla
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_data (
                    Date DATE NOT NULL,
                    Ticker VARCHAR(10) NOT NULL,
                    Open FLOAT,
                    High FLOAT,
                    Low FLOAT,
                    Close FLOAT,
                    Volume BIGINT,
                    PRIMARY KEY (Date, Ticker));
                    """)
            
            sql_insert = """
                INSERT INTO stock_data (Date, Close , High, Low, Open, Volume,Ticker)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE Open=VALUES(Open), High=VALUES(High), Low=VALUES(Low), Close=VALUES(Close), Volume=VALUES(Volume)
            """

            data["Ticker"] = ticker
            data = [
                        tuple(None if pd.isna(value) else value for value in row)
                        for row in data.itertuples(index=True, name=None)
                    ]
            connection.autocommit=True
            cursor.executemany(sql_insert, data)
            connection.commit()
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
