# Diagnóstico

## Fortalezas
- Se logró implementar una regresión lineal como modelo base.
- Se armó un pipeline inicial con ingesta de datos desde APIs (Yahoo Finance, FRED).
- Hubo buena coordinación para tener una primera entrega funcional.
- Se pudo captar la tendencia
- Ya contamos con una arquitectura definida
- Buen uso del backlog de tareas

# Debilidades
- El análisis comparativo fue limitado: de todos los modelos probados el mejor fue el de regresión lineal
- Los modelos de árboles fueron descartados por bajo rendimiento
- no se pudo captar la volatilidad y por ende no se captaron los picos extremos, que en análisis de riesgo son críticos
## Oportunidades de mejora
- Aplicación de modelos financieros (ej; ARIMA, GARCH, EGARCH, etc)
- Robustecer la ingesta de datos con fuentes alternativas

## Analisis de performance - BaseLine
Se entrenó un modelo de Regresión Lineal con horizontes de 5, 10 y 30 días. 
Métricas obtenidas (target a 30 días):
<img width="1575" height="632" alt="image" src="https://github.com/user-attachments/assets/35ec140a-503b-417e-89ed-a34cfe2059bf" />
- MAE: 0.02

### Interpretación
- Captura la tendencia general de la serie pero no la volatilidad
- Se asume que la regresión lineal supera a un predictor trivial (media)
- El modelo aporta valor como primer diagnóstico, pero aún tiene margen de mejora.


## Alcance MVP v1
El MVP debe ser simple pero funcional, mostrando valor rápidamente.

### P0 (Máxima prioridad):
| # Historia | Definición | DoD |
|------------|-----------|------|
|8-9|Como data scientist, quiero implementar un modelo ARCH/GARCH para capturar la volatilidad, de manera que el sistema pueda reflejar escenarios extremos con mayor realismo|Imagen con metricas y diagnostico en Historia|
|77|Como machine learning engineer quiero monitorear los entrenamientos de los modelos para poder garantizar la reproducibilidad de los mismos.|Pull request|

### P1 (Alta prioridad)
| # Historia | Definición | DoD |
|------------|------------|-----|
|10-11|Como data scientist, quiero entrenar modelos alternativos TGARCH y EGARCH, para evaluar si mejoran la captura de shocks asimétricos y colas pesadas respecto a GARCH.|Imagen con metricas y diagnostico en Historia|
|13|Como data machine learning engineer, quiero un sistema de monitoreo de pipelines y MAE, para asegurar que la ingesta, el entrenamiento y la performance del modelo se controlen de forma continua.|Pull Request|
|5| Como machine learning engineer, quiero contar con un dashboard en PowerBI, donde pueda visualizar de forma clara el desempeño del modelo y métricas clave, para facilitar la toma de decisiones.|Pull request|

