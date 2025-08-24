from cdc import get_cdc_date
from la_libreria.authentication import Credentials

creds = Credentials().load(path="Credentials/db_prod.json")

from carga_yahoo import cargar_datos_yahoo
from carga_fred import cargar_datos_fred

yahoo_date = get_cdc_date("sor_to_rdz ^GSPC")
fred_date = get_cdc_date("sor_to_rdz fred")

cargar_datos_yahoo(
    inicio=None,
    fin=None,
    credenciales=creds,
    ticker="^GSPC"
)

cargar_datos_fred(
    inicio=None,
    fin=None,
    credenciales=creds
)