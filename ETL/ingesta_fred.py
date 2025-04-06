def obtener_datos_fred(inicators = {
    'Unemployment Rate': 'UNRATE',
    'Federal Funds Rate': 'FEDFUNDS',
    '10-Year Treasury Rate': 'DGS10',
    'Industrial Production': 'INDPRO',
    'Personal Consumption': 'PCE',
    'Interest Rate': 'DFF',
    'Inflation': 'CPIAUCSL'},
    start=None,
    end=None):
    
    try:
        from fredapi import Fred
    except:
        import os
        os.system('pip install fredapi')
        from fredapi import Fred
    
    try:
        import pandas as pd
    except:
        import os
        os.system('pip install pandas')
        import pandas as pd

    fred = Fred(api_key='9eb5b198345d9bbad350ec5794c5d9d0')

    # Función para obtener datos de FRED
    def get_fred_data(series_id, frequency='d',start=None,end=None):
        # Obtener los datos de la serie de FRED
        data = fred.get_series(series_id, observation_start=start, observation_end=start)
        data = data.to_frame(name=series_id)
        data.index = pd.to_datetime(data.index)

        # Si la serie es mensual, cambiar la frecuencia a diaria sin llenar valores intermedios
        if frequency == 'm':
            data = data.resample('D').asfreq()  # Resamplear a diario pero sin rellenar con ffill()

        return data
    
    # obtener cada una de las series de indicadores
    data_frames = []
    for ind in inicators.values():
        try:
            # Obtener datos de cada indicador
            freq = 'm' if ind in ['UNRATE', 'CPIAUCSL', 'FEDFUNDS', 'INDPRO', 'PCE'] else 'd'
            df = get_fred_data(ind, frequency=freq,start=start,end=end)
            data_frames.append(df)
        except Exception as e:
            print(f"Error al obtener datos para el indicador {ind}: {e}")
            # En caso de error, continuar con el siguiente indicador
            continue
    
    
    # # Unir todos los DataFrames por el índice (fecha)
    # for i in range(1,len(data_frames)):
    #     try:
    #         data_frames[0] = data_frames[0].join(data_frames[i], how='outer')
    #     except Exception as e:
    #         print(f"Error al unir DataFrame {i}: {e}")
    #         continue
    # if len(data_frames) == 0:
    #     print("No se pudieron obtener datos de FRED para ninguno de los indicadores.")
    #     return None
    
    # Devolver el DataFrame combinado
    return data_frames