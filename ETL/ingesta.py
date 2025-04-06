


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

    # importar requests html
    try:
        from requests_html import HTMLSession
    except:
        import os
        os.system('pip install requests-html')
        from requests_html import HTMLSession

    """
    importar yahoo finance de yahoo_fin FIX
    try:
        import yahoo_fin as yf
    except:
        import os
        os.system('pip install yahoo_fin --upgrade')
        import yahoo_fin as yf

    # Descargar datos de Yahoo Finance
    from yahoo_fin.stock_info import get_stats
    data = get_stats('amzn')
    return data
    """

    #importar yahoo finance de yfinance
    try:
        import yfinance as yf
    except:
        import os
        os.system('pip install yfinance --upgrade')
        import yfinance as yf

    # Descargar datos de Yahoo Finance
    try:
        # Descargar datos de Yahoo Finance
        data = yf.download(ticker, start=inicio, end=fin,interval='1d')
        if data.empty:
            raise ValueError("No data found for the given date.")
        
        #ingestar a base de datos mysql
        from carga import cargar_datos
        cargar_datos(data,ticker=ticker,user=user,password=password,port=port,host=host)

        return data

    except Exception as e:
        print(f"Error downloading data: {e}")
        return None





#obtener la fecha de hoy
from datetime import datetime
#today = datetime.now().strftime('%Y-%m-%d')
ini= "2025-04-01"
fin= "2025-04-02"
data = obtener_datos(ini,fin)

print(data)
      
