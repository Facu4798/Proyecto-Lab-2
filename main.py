from buscar_prediccion import buscar_prediccion

#input
dias = input("a cuantos dias quiere estimar el riesgo?")

#buscar la predicción en la base de datos
prediccion = buscar_prediccion(fecha,dias)

print(f"el value at risk(VaR) a {dias} dias es {prediccion}")
