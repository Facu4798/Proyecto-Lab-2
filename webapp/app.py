#set working directory to current file
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from flask import Flask, render_template, request, jsonify
from obtener_datos import obtener_datos

app = Flask(__name__)

# Cambiá estos datos por los reales de tu base MySQL
DB_CONFIG = {
    "user": "avnadmin",
    "host": "estrie01-estimacionderiego1.j.aivencloud.com",
    "password": "AVNS_vBt5bLw5TLinvY6G_Eo",
    "port": 24195,
    "database": "defaultdb"
}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    query = "SELECT * FROM predicciones ORDER BY Date DESC LIMIT 1"
    df = obtener_datos(query, **DB_CONFIG)
    
    if df.empty:
        return jsonify({"error": "No se encontraron datos"}), 404

    fila = df.iloc[0]

    def prediction_hash(p)->str:
        import numpy as np
        if p > 0:
            return str(0)+"%"
        else:
            p = abs(p)
            p2 =str(np.round(p*100, 2))+"%"
            if p2.split(".")[1].split("%")[0] == "0" or p2.split(".")[1].split("%")[0] == "00":
                return p2.split(".")[0]+"%"
            else:
                return p2
        


    datos = {
        "Ticker": fila["Ticker"],
        "5Days": prediction_hash(fila["5Days"]),
        "10Days": prediction_hash(fila["10Days"]),
        "30Days": prediction_hash(fila["30Days"])
    }

    

    return jsonify(datos)

if __name__ == "__main__":
    app.run(debug=True)
