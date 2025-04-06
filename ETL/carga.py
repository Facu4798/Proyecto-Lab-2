def cargar_datos(data,
                 user = 'root',
                 password = 'password',
                 port=3306, 
                 host='localhost',
                 ticker='TSLA'):
    """
    Esta función carga los datos a la base de datos MySQL 
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

                # Verificar si la tabla existe, si no, crearla
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS stock_data (
                        Date DATE NOT NULL,
                        Ticker VARCHAR(10) NOT NULL,
                        Open FLOAT,
                        High FLOAT,
                        Low FLOAT,
                        Close FLOAT,
                        Volume INT,
                        PRIMARY KEY (Date, Ticker));
                        """)

                # Insertar datos en la tabla
                for index, row in data.iterrows():
                    cursor.execute("""
                        INSERT INTO stock_data (Date,Ticker, Open, High, Low, Close, Volume)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE Open=%s, High=%s, Low=%s, Close=%s, Volume=%s
                    """, (index.strftime('%Y-%m-%d'),ticker, row['Open'], row['High'], row['Low'], row['Close'], int(row['Volume']), row['Open'], row['High'], row['Low'], row['Close'], int(row['Volume'])))
                
                connection.commit()
    except:
        raise ValueError("no se pudo establecer una coenexión a la base de datos")
    finally:
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