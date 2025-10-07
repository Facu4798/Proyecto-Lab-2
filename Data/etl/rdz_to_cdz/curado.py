def curar():
    import sys
    import os
    import pandas as pd
    from la_libreria.utils import substract_date,get_ts, parse_query
    from la_libreria.authentication import Credentials
    from la_libreria.connectors import MySQLConnector
    from cdc_l2 import get_cdc_date
    os.system("clear")

    # leer las credenciales de la base de datos
    try:
        creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_dev.json")
    except: 
        sys.exit("Credentials file not found")



    # parametros de la corrida
    shift = 35
    cdc_date = get_cdc_date("rdz_to_cdz",creds=creds)


    if cdc_date is not None:
        cdc_date = substract_date(date_str=str(cdc_date),
                                amount=shift,
                                interval="d")
    ticker="^GSPC"



    # leer el archivo de la query
    try:
        query_path = "/workspaces/Proyecto-Lab-2/Data/etl/rdz_to_cdz/union copy 2.sql"
        if cdc_date is not None:
            q = parse_query(query_path,
                            replacement_dict={"date_placeholder":cdc_date,"ticker_placeholder":ticker})
        else:
            q = parse_query(query_path,
                            replacement_dict={"Date >= 'date_placeholder'":"1=1","ticker_placeholder":ticker})
        
    except Exception as e:
        sys.exit(e)

    # obtener los datos de rdz
    try:
        conn = MySQLConnector(creds.dict)
        conn.connect()
        data = conn.get_data(query=q)
        data["etl_ts"] = str(get_ts())
        conn.close()
    except Exception as e:
        sys.exit(e)


    # intentar crear la tabla curated
    try:
        conn = MySQLConnector(creds.dict)
        conn.connect()
        conn.create_table(data=data,table_name="curated",pks=["Date","Ticker"],exceptions={"Volume":"BIGINT"})
        conn.close()
    except Exception as e:
        print(e)


    # guardar los datos en cdz y el watermark
    try:
        conn = MySQLConnector(creds.dict)
        conn.connect()
        conn.insert_data(data=data,table_name="curated",pks=["Date","Ticker"])
        last_date = str(data.iloc[-1]["Date"])
        conn.insert_data(data=pd.DataFrame(
            {
                "description":["rdz_to_cdz ^GSPC"],
                "date":[last_date]
            }),
            table_name="cdc",pks=["description"]
        )
        conn.close()
    except Exception as e:
        sys.exit(e)




