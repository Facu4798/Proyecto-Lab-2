def obtener_datos_yahoo(start=None, end=None,
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
        data = yf.download(ticker, start=start, end=end,interval='1d')
        if data.empty:
            raise ValueError("No data found for the given date.")
        
        # Eliminar la segunda fila de columnas
        data.columns = data.columns.droplevel(1)
        data.columns = [i for i in data.columns]
        data.index = [i for i in data.index]

        return data
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None
