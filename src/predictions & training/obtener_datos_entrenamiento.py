

def obtener_datos_entrenamiento(start,
                                end,
                                database,
                                host,
                                user,
                                password,
                                port,
                                dias,
                                ticker):
    #import mysql.connector
    try:
        import mysql.connector
    except ImportError:
        import os
        os.system("pip install mysql-connector-python")
        import mysql.connector

    #import pandas
    try:
        import pandas as pd
    except ImportError:
        import os
        os.system("pip install pandas")
        import pandas as pd

    #import joblib
    try:
        import joblib
    except ImportError:
        import os
        os.system("pip install joblib")
        import joblib


    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )

    query = f"""SELECT * FROM delivery
                WHERE Ticker = '{ticker}'
                AND Date >= '{start}'
                AND Date <= '{end}'"""
    
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = pd.DataFrame(data, columns=columns)

    
    try:
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
    except:
        pass
    cursor.close()
    connection.close()
    return data