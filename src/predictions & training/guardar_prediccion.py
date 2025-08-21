def guardar_prediccion(p5,
                       p10,
                       p30,
                       date,
                       user,
                       password,
                       host,
                       port,
                       database,
                       ticker="^GSPC"):
    

    
    import mysql.connector
    import pandas as pd


    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )
    cursor = connection.cursor()
    cursor.execute("USE defaultdb")

    # crear la tabla si no existe
    sql = """
    CREATE TABLE IF NOT EXISTS predicciones (
        Date DATE NOT NULL,
        Ticker VARCHAR(10) NOT NULL,
        5Days FLOAT DEFAULT NULL,
        10Days FLOAT DEFAULT NULL,
        30Days FLOAT DEFAULT NULL,
        PRIMARY KEY (Date, Ticker)
    )
    """
    
    cursor.execute(sql)

    connection.commit()

    sql = f"""
    INSERT INTO predicciones (Date, Ticker, 5Days, 10Days, 30Days)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 5Days = VALUES(5Days), 10Days = VALUES(10Days), 30Days = VALUES(30Days)
    """
    # Insertar los datos en la tabla
    cursor.execute(sql, (date, ticker, p5, p10, p30))
    connection.commit()

    # Cerrar la conexión
    cursor.close()
    connection.close()

