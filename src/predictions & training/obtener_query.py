def obtener_query(file_path,start_date):
    """
    Esta función lee un archivo SQL y devuelve su contenido como una cadena.
    """
    with open(file_path, 'r') as file:
        query = file.read()
        if start_date!=None:
            query = query.replace("date_placeholder", start_date)
        else:
            #get position of "WHERE"
            where_pos = query.find("WHERE")
            query = query[:where_pos] + ";"
    return query