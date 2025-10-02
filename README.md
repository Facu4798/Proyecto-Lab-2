# Estimación de riesgo

**Autores:**
- Facundo Mazzola *facundomazzola@uca.edu.ar*
- Matias Fabian Adell *matiasadell@uca.edu.ar*
- Pedro Naon *pedronaon@uca.edu.ar*
- Matias Roberti *matiasroberti@uca.edu.ar*
- Agustin Peña *agustinpena@uca.edu.ar*

## Descripción general del proyecto
El proyecto presenta una aplicación web que muestra predicciones de un modelo de machine learning sobre el riesgo de la acción *S&P500* a 5, 10 y 30 días.




### Objetivos

El objetivo de este proyecto es poder predecir el riesgo a 5, 10 y 30 dias para la acción *S&P500*. El riesgo o Value at Risk(VaR) se calcula en este caso como la variación porcentual entre el minimo valor entre los proximos 5, 10 o 30 días respecto del valor actual. 

$$\text{Riesgo(dias)}=\frac{\text{MenorValor(dias)}}{\text{Valor Actual}}$$

### Fuentes de datos
Para realizar el proyecto se obtuvieron datos de la acción de la API de Yahoo Finance y datos macroeconómicos de Estados Unidos de la API FRED.

### Aplicación pretendida
Se pretende que el modelo se utilize como feature en una aplicación de trading, para que los usuarios puedan consultarlo, y así, informarse sobre el posible riesgo de las acciones en las que pretenden invertir.

### Estrategia de puesta en producción de modelo
Ante la presencia de predicciones extremas o fuera de lo normal el reemplazo por el modelo del dia anterior con su horizonte de prediccion ajustado a la nueva fecha a predecir.


## Contenidos

A continuación se explican los contenidos de cada una de las carpetas en el proyecto:

### `docs`
Esta carpeta incluye la documentación de los procesos de ingesta de datos, la arquitectura del proyecto, 

### `data`
Esta carpeta incluye los códigos que se utilizan para realizar la ingesta de datos


### `models`
Esta carpeta almacena los modelos generados en formato `*.joblib`

### `notebooks`
Esta carpeta contiene todas las notebooks(archivos `*.ipynb`) que se utilizaron para explorar los datos, crear los modelos y diseñar cada una de las features incluidas en los modelos. Su función es servir de herramienta de experimentación para los data scientists. 

### `src`
Esta carpeta contiene los códigos de entrenamiento y predicción de los modelos.

### `requirements.pdf`
El archivo contiene los requisitos de software que se deben tener para poder ejecutar el proyecto.
