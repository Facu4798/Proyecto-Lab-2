def cargar_datos(df,user,password,host,port,database):
    """
    Esta función carga un DataFrame en una tabla de una base de datos mysql.
    """

    try:
        import pandas as pd
    except ImportError:
        import os
        os.system('pip install pandas')
        import pandas as pd
    
    #import mysql.connector
    try:
        import mysql.connector
    except ImportError:
        import os
        os.system('pip install mysql-connector-python')
        import mysql.connector

    # Create a connection to the database
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Create a table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS curated (
            Date DATE,
            Ticker VARCHAR(10),
            Open FLOAT,
            Close FLOAT,
            High FLOAT,
            Low FLOAT,
            Volume BIGINT,
            CPI FLOAT,
            Unemployment FLOAT,
            Industrial_production FLOAT,
            Fed_funds_rate FLOAT,
            10_year_treasury FLOAT,
            PCE FLOAT,
            DFF FLOAT,
            Target5 FLOAT,
            Target10 FLOAT,
            Target30 FLOAT, 
            PRIMARY KEY (Date, Ticker)
        )
    """)

    # prepare the data for insertion

    df = df.copy()
    df.index = df.index.astype(str)
    print(len(df.columns))
    df = [
        tuple(None if pd.isna(value) else value for value in row)
        for row in df.itertuples(index=True, name=None)
    ]

    if len(df[0])==17:
        print("Las columnas estan bien")
    else:
        print("Las columnas no son las correctas")
        print(df[0])
        raise ValueError("Las columnas no son las correctas")

    # Prepare the insert query
    insert_query = """
        INSERT INTO curated (Date, Ticker, Open, Close, High, Low, Volume, CPI, Unemployment, Industrial_production, Fed_funds_rate, 10_year_treasury, PCE, DFF, Target5, Target10, Target30)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        ON DUPLICATE KEY UPDATE
            Open=VALUES(Open),
            Close=VALUES(Close),
            High=VALUES(High),
            Low=VALUES(Low),
            Volume=VALUES(Volume),
            CPI=VALUES(CPI),
            Unemployment=VALUES(Unemployment),
            Industrial_production=VALUES(Industrial_production),
            Fed_funds_rate=VALUES(Fed_funds_rate),
            10_year_treasury=VALUES(10_year_treasury),
            PCE=VALUES(PCE),
            DFF=VALUES(DFF),
            Target5=VALUES(Target5),
            Target10=VALUES(Target10),
            Target30=VALUES(Target30)
    """
    # Execute the insert query
    cursor.executemany(insert_query, df)
    # Commit the changes
    connection.commit()
    # Close the cursor and connection
    cursor.close()
    connection.close()
