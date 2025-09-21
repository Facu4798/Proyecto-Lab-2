from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector

creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_prod.json")
conn = MySQLConnector(creds.dict)
conn.connect()
data = conn.get_data("""
SELECT  src.Date,
        src.Ticker,
        src.Open,
        src.Close,
        src.High,
        src.Low,
        src.Volume,
        (src.Open - src.Close) AS retorno,
        (src.Open - src.Close) / src.Open AS retorno_porcentaje,
        ABS(src.High - src.Low) AS amplitud,
        ABS(src.High - src.Low) / src.Open AS amplitud_porcentaje,
        src.CPI,
        src.Unemployment,
        src.Industrial_production,
        src.Fed_funds_rate,
        src.10_year_treasury,
        src.PCE,
        src.DFF,
        src.Target5,
        src.Target10,
        src.Target30
FROM curated as src
WHERE src.Date >= '1995-01-01'
""")
conn.close()
print(data)