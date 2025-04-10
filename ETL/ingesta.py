


def obtener_datos(inicio, fin,
                  ticker='TSLA',
                  user='root', 
                  password='password',
                  port=3306,
                  host='localhost'):
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


    #validacion de fechas
    if not isinstance(inicio, str) or not isinstance(fin, str):
        raise ValueError("Las fechas deben ser cadenas en formato 'YYYY-MM-DD'")
    if inicio >= fin:
        raise ValueError("La fecha de inicio debe ser menor que la fecha de fin")

    #ingestar los datos de yahoo finance
    from ingesta_yahoo import obtener_datos_yahoo
    try:
        data_yahoo = obtener_datos_yahoo(
            ticker=ticker,
            start=inicio,
            end=fin,
            user=user, 
            password=password,
            port=port,
            host=host
        )
    except:
        print("Error al obtener datos de Yahoo Finance")
        data_yahoo = None

    #cargar los datos de yahoo a la base de datos mysql





    #ingestar los datos de FRED
    from ingesta_fred import obtener_datos_fred
    try:
        data_fred = obtener_datos_fred(start=inicio,
                                       end=fin)
    except:
        print("error al obtener datos de FRED")
        data_fred = None


    # cargar los datos de FRED en la base de datos mysql serie a serie
    from carga_fred import cargar_datos_fred
        try:
            cargar_datos_fred(data=data_fred,
                                user=user,
                                password=password,
                                port=port,
                                host=host)
        except Exception as e:
            print(f"Error al cargar datos de FRED a la base de datos MySQL: {e}")
            # Continuar con el siguiente conjunto de datos

    return {"datos yahoo": data_yahoo,"datos_fred":data_fred}


datos = obtener_datos(inicio='2023-01-01', fin='2023-12-31', ticker='TSLA')
print(datos)