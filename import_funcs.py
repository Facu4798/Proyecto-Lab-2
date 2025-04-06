#importar pandas
def import_pandas():
    try:
        import pandas as pd
    except:
        import os
        os.system('pip install pandas')
        import pandas as pd

#importar yahoo fineance de yfinance
def import_yfinance():
    try:
        import yfinance as yf
    except:
        import os
        os.system('pip install yfinance --upgrade')
        import yfinance as yf

#importar conector a mysql
def import_mysql_connector():
    try:
        import mysql.connector
        from mysql.connector import Error
    except:
        import os
        os.system('pip install mysql-connector-python')
        import mysql.connector
        from mysql.connector import Error

