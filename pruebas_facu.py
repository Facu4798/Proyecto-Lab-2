from fredapi import Fred
import pandas as pd
import requests
#importar datos del pbi

# Descargar datos del PBI de Estados Unidos
# Realizar la solicitud a la API de FRED



indicators = {
    'Unemployment Rate': 'UNRATE',
    'Federal Funds Rate': 'FEDFUNDS',
    '10-Year Treasury Rate': 'DGS10',
    'Industrial Production': 'INDPRO',
    'Personal Consumption': 'PCE',
    'Interest Rate': 'DFF',
    'Inflation': 'CPIAUCSL'
}

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

data = get_fred_data('UNRATE', frequency='m')
print(data)