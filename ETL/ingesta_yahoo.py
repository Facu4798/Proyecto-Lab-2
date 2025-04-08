def obtener_datos_yahoo(inicio, fin,
                        ticker='TSLA',
                        user='root',
                        password='password',
                        port=3306,
                        host='localhost'):


    #importar pandas
    try:
        import pandas as pd
    except:
        import os
        os.system('pip install pandas')
        import pandas as pd

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
        
        # Eliminar la segunda fila de columnas
        data.columns = data.columns.droplevel(1)

        #ingestar a base de datos mysql
        from ETL.carga_yahoo import cargar_datos
        try:
            cargar_datos(data,ticker=ticker,user=user,password=password,port=port,host=host)
        except:
            print("Error al cargar los datos a la base de datos MySQL")

        return data
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None