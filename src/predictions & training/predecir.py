#set working directory to current file
import os
import sys

# if linux, clear else cls
if sys.platform.startswith('linux'):
    os.system('clear')
else:
    os.system('cls')

predictions_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(predictions_path)
head_path = os.path.dirname(src_path)
print(f"src_path: {head_path}")




def predecir(modelo,
             database,
             host,
             port,
             user,
             password,
             ticker,
             train=True):
    


    import os
    os.system("cls")

    #import pandas
    try:
        import pandas as pd
    except ImportError:
        import os
        os.system('pip install pandas')
        import pandas as pd

    #import joblib
    try:
        import joblib
    except ImportError:
        import os
        os.system('pip install joblib')
        import joblib


    from obtener_datos import obtener_datos
    from obtener_query import obtener_query

    if train:
        query_path = f"{predictions_path}/get_all.sql"
    else:
        query_path = f"{predictions_path}/get_last.sql"
    
    df = obtener_datos(obtener_query(file_path=query_path,start_date="1995-01-01"),
                       user=user,
                       host=host,
                       password=password,
                       port=port,
                       database=database)
    
    from transformar_datos import transformar_datos
    df,columns_to_drop = transformar_datos(df)
    df = df.drop(columns=["Ticker"])

    def get_drops(df,days):
        drops = []
        for col in df.columns:
            if col.startswith("Target") and str(days) not in col:
                drops.append(col)
        return drops
    

    # prediccion 5 dias
    if train:
        model5 = modelo
        model5.fit(
            df.drop(columns=get_drops(df, 5)).iloc[:-5], 
            df["Target5"].iloc[:-5]
        )
        joblib.dump(model5, f"{head_path}models/modelo_5_{ticker}.joblib")
    else:
        model5 = joblib.load(f"{head_path}models/modelo_5_{ticker}.joblib")

    p5 = model5.predict(df.tail(1).drop(columns=get_drops(df,5)))[0]


    # prediccion 10 dias
    if train:
        model10 = modelo
        model10.fit(
            df.drop(columns=get_drops(df, 10)).iloc[:-10], 
            df["Target10"].iloc[:-10]
        )
        joblib.dump(model10, f"{head_path}models/modelo_10_{ticker}.joblib")
    else:
        model10 = joblib.load(f"{head_path}models/modelo_10_{ticker}.joblib")

    p10 = model10.predict(df.tail(1).drop(columns=get_drops(df,10)))[0]

    # prediccion 30 dias
    if train:
        model30 = modelo
        model30.fit(
            df.drop(columns=get_drops(df, 30)).iloc[:-30], 
            df["Target30"].iloc[:-30]
        )
        joblib.dump(model30, f"{head_path}models/modelo_30_{ticker}.joblib")
    else:
        model30 = joblib.load(f"{head_path}models/modelo_30_{ticker}.joblib")

    p30 = model30.predict(df.tail(1).drop(columns=get_drops(df,30)))[0]

    from guardar_prediccion import guardar_prediccion
    guardar_prediccion(
        date = df.index[-1],
        ticker=ticker,
        p5=p5,
        p10=p10,
        p30=p30,
        user=user,
        host=host,
        password=password,
        port=port,
        database=database
    )


try:
    from sklearn.linear_model import LinearRegression
except:
    import os
    os.system('pip install scikit-learn')
    from sklearn.linear_model import LinearRegression


model = LinearRegression()


predecir(
    host="estrie01-estimacionderiego1.j.aivencloud.com",
    user="avnadmin",
    password="AVNS_vBt5bLw5TLinvY6G_Eo",
    port=24195,
    database="defaultdb",
    modelo=model,
    ticker="^GSPC",
    train=True
)
        