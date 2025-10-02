#set working directory to current file
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from flask import Flask, render_template, request, jsonify
from obtener_datos import obtener_datos
from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector
creds = Credentials().load(path="/workspaces/Proyecto-Lab-2/Credentials/db_dev.json")
conn = MySQLConnector(creds.dict)
conn.connect()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    query = "SELECT * FROM predicciones ORDER BY Date DESC LIMIT 1"
    # df = obtener_datos(query, **DB_CONFIG)
    df = conn.get_data(query)
    print(df)
    if df.empty:
        return jsonify({"error": "No se encontraron datos"}), 404

    fila = df.iloc[0]

    def prediction_hash(p)->str:
        import numpy as np
        return str(np.round(p, 2))+"%"
        


    datos = {
        "Ticker": fila["Ticker"],
        "5Days": prediction_hash(fila["5Days"]),
        "10Days": prediction_hash(fila["10Days"]),
        "30Days": prediction_hash(fila["30Days"])
    }
    print(datos)

    

    return jsonify(datos)

if __name__ == "__main__":
    app.run(debug=True)
