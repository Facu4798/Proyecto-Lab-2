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
    
    import time
    from model_tracking import model_tracking_insert
    from sklearn.metrics import mean_absolute_error
    from la_libreria.utils import get_ts

    # prediccion 5 dias
    if train:
        model5 = modelo
        t_start5 = time.time()
        model5.fit(
            df.drop(columns=get_drops(df, 5)).iloc[:-5], 
            df["Target5"].iloc[:-5]
        )
        t_train5 = time.time() - t_start5
        joblib.dump(model5, f"{head_path}/Models/modelo_5_{ticker}.joblib")
    else:
        model5 = joblib.load(f"{head_path}/Models/modelo_5_{ticker}.joblib")

    t_start_p5 = time.time()
    p5 = model5.predict(df.tail(1).drop(columns=get_drops(df,5)))[0]
    t_pred5 = time.time() - t_start_p5


    if train:
        model_tracking_insert(
            timestamp=t_start5,
            target="5",
            nombre_modelo=model5.__class__.__name__,
            n_train=df.shape[0],
            n_test=1,
            features=df.drop(columns=["Target5", "Target10", "Target30"]).columns.tolist(),
            parametros=model5.get_params(),
            metrics={
                "mae": None
            },
            last_date=df.index[-1],
            first_date=df.index[0],
            ticker=ticker,
            training_time= t_train5,
            prediction_time= t_pred5
        )
    
    # prediccion 10 dias
    if train:
        model10 = modelo
        t_start10 = time.time()
        model10.fit(
            df.drop(columns=get_drops(df, 10)).iloc[:-10], 
            df["Target10"].iloc[:-10]
        )
        t_train10 = time.time() - t_start10
        joblib.dump(model10, f"{head_path}/Models/modelo_10_{ticker}.joblib")
    else:
        model10 = joblib.load(f"{head_path}/Models/modelo_10_{ticker}.joblib")

    t_start_p10 = time.time()
    p10 = model10.predict(df.tail(1).drop(columns=get_drops(df,10)))[0]
    t_pred10 = time.time() - t_start_p10

    if train:
        model_tracking_insert(
            timestamp=t_start10,
            target="10",
            nombre_modelo=model10.__class__.__name__,
            n_train=df.shape[0],
            n_test=1,
            features=df.drop(columns=["Target5", "Target10", "Target30"]).columns.tolist(),
            parametros=model10.get_params(),
            metrics={
                "mae": None
            },
            last_date=df.index[-1],
            first_date=df.index[0],
            ticker=ticker,
            training_time= t_train10,
            prediction_time= t_pred10
        )

    # prediccion 30 dias
    if train:
        model30 = modelo
        t_start30 = time.time()
        model30.fit(
            df.drop(columns=get_drops(df, 30)).iloc[:-30], 
            df["Target30"].iloc[:-30]
        )
        t_train30 = time.time() - t_start30
        joblib.dump(model30, f"{head_path}/Models/modelo_30_{ticker}.joblib")
    else:
        model30 = joblib.load(f"{head_path}/Models/modelo_30_{ticker}.joblib")

    t_start_p30 = time.time()
    p30 = model30.predict(df.tail(1).drop(columns=get_drops(df,30)))[0]
    t_pred30 = time.time() - t_start_p30

    if train:
        model_tracking_insert(
            timestamp=t_start30,
            target="30",
            nombre_modelo=model30.__class__.__name__,
            n_train=df.shape[0],
            n_test=1,
            features=df.drop(columns=["Target5", "Target10", "Target30"]).columns.tolist(),
            parametros=model30.get_params(),
            metrics={
                "mae": None
            },
            last_date=df.index[-1],
            first_date=df.index[0],
            ticker=ticker,
            training_time= t_train30,
            prediction_time= t_pred30
        )


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


from la_libreria.authentication import Credentials
creds = Credentials().load(path="Credentials/db_prod.json").dict

predecir(
    host=creds["host"],
    user=creds["user"],
    password=creds["password"],
    port=creds["port"],
    database=creds["database"],
    modelo=model,
    ticker="^GSPC",
    train=True
)
        
