from buscar_prediccion import buscar_prediccion

#input
dias = input("a cuantos dias quiere estimar el riesgo?")

from datetime import datetime
fecha = datetime.now().strftime('%d-%m-%Y')

#buscar la predicción en la base de datos
prediccion = buscar_prediccion(fecha,dias)

print(f"el value at risk(VaR) a {dias} dias es {prediccion}")
