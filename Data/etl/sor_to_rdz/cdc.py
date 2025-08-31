
def get_cdc_date(desc):
    from la_libreria.authentication import Credentials
    from la_libreria.connectors import MySQLConnector

    creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_prod.json")
    conn = MySQLConnector(creds.dict)
    conn.connect()
    try:
        return conn.get_data(query=f"SELECT date FROM cdc WHERE description = '{desc}'").head(1).iloc[0,0]
    except:
        return None
        
