import joblib
import datetime
from get_last_model import get_last_model

def generar_prediccion(modelo,models_dir,train,days,ticker,data):


    if train:
        x = data.drop(columns=[i for i in data.columns if i.startswith("Target")])
        x = x.iloc[:-days,:]
        y = data[f"Target{days}"]
        y = y.iloc[:-days]

        modelo.fit(x,y)

        now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        joblib.dump(modelo,f"{models_dir}modelo_{days}_{ticker}_{now}.joblib")
    else:
        modelo = get_last_model(ticker,days)

    pred = modelo.predict(x.iloc[-1,:])[0]
    return [x.iloc[-1,:]["Date"], pred]