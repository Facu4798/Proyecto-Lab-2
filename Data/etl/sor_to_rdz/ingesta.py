from cdc import get_cdc_date
from la_libreria.utils import substract_date
from la_libreria.authentication import Credentials
import os
os.system("clear")

try:
    creds = Credentials().load(path="Credentials/db_dev.json")
except:
    raise Exception("No se pudo cargar las credenciales")

from carga_yahoo import cargar_datos_yahoo
from carga_fred import cargar_datos_fred

try:
    yahoo_date = get_cdc_date("sor_to_rdz ^GSPC",creds=creds)
    if yahoo_date is not None:
        yahoo_date = substract_date(date_str = str(yahoo_date))
    else:
        yahoo_date = "1900-01-01"

    cargar_datos_yahoo(
        inicio=yahoo_date,
        fin=None,
        credentials=creds,
        ticker="^GSPC"
    )
except Exception as e:
    print(e)

try:
    fred_date = get_cdc_date("sor_to_rdz fred",creds=creds)
    if fred_date is not None:
        fred_date = substract_date(date_str = str(fred_date))


    cargar_datos_fred(
        inicio=fred_date,
        fin=None,
        credentials=creds
    )
except Exception as e:
    print(e)