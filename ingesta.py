

def obtener_datos(fecha):
    #importar pandas
    try:
        import pandas as pd
    except:
        import os
        os.system('pip install pandas')
        import pandas as pd

    #importar yahoo finance
    try:
        import yahoo_fin as yf
    except:
        import os
        os.system('pip install yahoo_fin')
        import yahoo_fin as yf

    # Descargar datos de Yahoo Finance

#obtener la fecha de hoy
from datetime import datetime
today = datetime.now().strftime('%d-%m-%Y')

data = obtener_datos(today)
      
