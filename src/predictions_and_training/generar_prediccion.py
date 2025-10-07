import joblib
import datetime
from get_last_model import get_last_model
from transformar_datos import transformar_datos
from model_tracking import model_tracking_insert


def generar_prediccion(modelo,models_dir,train,days,ticker,data):
    
    pred_date = data.tail(1)["Date"].values[0]

    if train:
        first_date = data.head(1)["Date"].values[0]
        last_date = data.tail(1)["Date"].values[0]


    data = data.drop(columns=["Date","Ticker"])

    data,ctd = transformar_datos(data)
    data = data.drop(columns=ctd)

    x = data.drop(columns=[i for i in data.columns if i.startswith("Target")])
    x = x.iloc[:-days,:]
    y = data[f"Target{days}"]
    y = y.iloc[:-days]

    if train:
        n_train = len(y)
        tt_0 = datetime.datetime.now()
        modelo.fit(y=y,x=None)
        tt = (datetime.datetime.now() - tt_0).total_seconds()

        now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        joblib.dump(modelo,f"{models_dir}modelo_{days}_{ticker}_{now}.joblib")
    else:
        modelo = get_last_model(ticker,days)
        n_train = 0
        first_date = None
        last_date = None

    pt_0 = datetime.datetime.now()
    # pred = modelo.predict(x.tail(1))[0]
    pred = modelo.predict(steps=days, exog_future=None)[-1]
    pt = (datetime.datetime.now() - pt_0).total_seconds()

    model_tracking_insert(timestamp=datetime.datetime.now(),
                        target=days,
                        ticker=ticker,
                        nombre_modelo=modelo.__str__(),
                        n_train=n_train,
                        n_test=1,
                        first_date=first_date,
                        last_date=last_date,
                        training_time=tt,
                        prediction_time=pt,
                        parametros=modelo.get_params(),
                        features=",".join(x.columns),
                        metrics={"MAE":None})

    return [pred_date, pred]