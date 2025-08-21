
def obtener_datos(inicio=None, fin=None,
                  ticker='TSLA',
                  user='root', 
                  password='password',
                  port=3306,
                  host='localhost',
                  database='risk-estimate-dl'):
    """
    Esta función obtiene datos de Yahoo Finance para un rango de fechas específico e
    ingesta los datos en una base de datos MySQL.
    **Parámetros:**
    - **inicio:** str, fecha de inicio en formato 'YYYY-MM-DD'
    - **fin:** str, fecha de fin en formato 'YYYY-MM-DD'
    - **user:** str, usuario de MySQL (default='root')
    - **password:** str, contraseña de MySQL (default='password')
    - **port:** int, puerto de MySQL (default=3306)
    - **host:** str, host de MySQL (default='localhost')
    - **ticker:** str, ticker de la acción (default='TSLA')
    **Retorna:**
    - **data:** DataFrame con los datos descargados de Yahoo Finance
    """  
    import io
    import requests
    import ftplib

    #importar pandas
    try:
        import pandas as pd
    except:
        import os
        os.system('pip install pandas')
        import pandas as pd


    #validacion de fecha
    if inicio is None or fin is None:
        pass
    elif not isinstance(inicio, str) or not isinstance(fin, str):
        raise ValueError("Las fechas deben ser cadenas en formato 'YYYY-MM-DD'")
    elif inicio >= fin:
        raise ValueError("La fecha de inicio debe ser menor que la fecha de fin")

    #ingestar los datos de yahoo finance
    from ingesta_yahoo import obtener_datos_yahoo
    data_yahoo = obtener_datos_yahoo(
        ticker=ticker,
        start=inicio,
        end=fin,
    )
    

    #cargar los datos de yahoo a la base de datos mysql

    from carga_yahoo import cargar_datos_yahoo
    cargar_datos_yahoo(data=data_yahoo,
                        user=user,
                        password=password,
                        port=port,
                        host=host,
                        ticker=ticker)


    #ingestar los datos de FRED
    from ingesta_fred import obtener_datos_fred
    data_fred = obtener_datos_fred(start=inicio,
                                       end=fin)


    # cargar los datos de FRED en la base de datos mysql serie a serie
    from carga_fred import cargar_datos_fred
    cargar_datos_fred(data=data_fred,
                            user=user,
                            password=password,
                            port=port,
                            host=host,
                            database=database)

    return {"datos yahoo": data_yahoo,"datos_fred":data_fred}

import pandas as pd
from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')
tomorrow = (datetime.today() + pd.DateOffset(days=1)).strftime('%Y-%m-%d')

obtener_datos(inicio=None,fin=None
            ,ticker='^GSPC',
            host="estrie01-estimacionderiego1.j.aivencloud.com",
            user="avnadmin",
            password="AVNS_vBt5bLw5TLinvY6G_Eo",
            port=24195,
            database="defaultdb")
