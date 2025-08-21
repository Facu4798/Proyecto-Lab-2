
def generar_prediccion(ticker,
                        dias,
                        database,
                        host,
                        user,
                        password,
                        port,
                        model_obj):
    
    from obtener_ultima_fila import obtener_ultima_fila
    data = obtener_ultima_fila(database, host, user, password, port, ticker)
    
    if data.empty:
        print("No hay datos para generar la predicción.")
        return None
    
    drops = [col for col in data.columns if col.startswith("Target")]
    # Preprocesar los datos si es necesario
    data = data.drop(columns=drops)
    
    # Realizar la predicción
    prediccion = model_obj.predict(data)
    
    return prediccion[0]  # Retornar el valor de la predicción

