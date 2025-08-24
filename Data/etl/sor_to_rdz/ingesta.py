from cdc import get_cdc_date
from la_libreria.utils import substract_date
from la_libreria.authentication import Credentials

creds = Credentials().load(path="Credentials/db_prod.json")

from carga_yahoo import cargar_datos_yahoo
from carga_fred import cargar_datos_fred

yahoo_date = get_cdc_date("sor_to_rdz ^GSPC")
yahoo_date = substract_date(date_str = str(yahoo_date))
fred_date = get_cdc_date("sor_to_rdz fred")
fred_date = substract_date(date_str = str(fred_date))

cargar_datos_yahoo(
    inicio=None,
    fin=None,
    credentials=creds,
    ticker="^GSPC"
)

cargar_datos_fred(
    inicio=None,
    fin=None,
    credentials=creds
)