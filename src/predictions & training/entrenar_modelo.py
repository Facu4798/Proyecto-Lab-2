from sklearn.linear_model import LinearRegression


model = LinearRegression()



def entrenar_modelo(ticker,
                    dias,
                    start,
                    end,
                    databse,
                    host,
                    user,
                    password,
                    port,model_obj):

    from obtener_datos_entrenamiento import obtener_datos_entrenamiento

    try:
        import joblib
    except ImportError:
        import os
        os.system('pip install joblib')
        import joblib
    
    data = obtener_datos_entrenamiento(start, end, databse, host, user, password, port, dias, ticker)
    if data.empty:
        print("No hay datos para entrenar el modelo.")
        return None
    
    drops = [col for col in data.columns if ((col.startswith("Target")) and (f"{dias}" not in col))]
    data = data.drop(columns=drops)
    model_obj.fit(data.drop(columns=f"Target{dias}"),data[f"Target{dias}"])
    
    # get current date
    import datetime
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # save the model
    joblib.dump(model_obj, f"models/modelo_{ticker}_{dias}_{current_date}.joblib")





    

















