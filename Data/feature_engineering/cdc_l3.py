def get_cdc_date(desc,creds=None,conn=None):
    from la_libreria.authentication import Credentials
    from la_libreria.connectors import MySQLConnector

    # conn = MySQLConnector(creds.dict)
    # conn.connect()
    try:
        cdc_date =conn.get_data(query=f"SELECT * FROM cdc WHERE description = '{desc}'").head(1).iloc[0,1]
        # conn.close()
    except:
        cdc_date = None
    return cdc_date