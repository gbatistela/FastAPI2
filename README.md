# Proyecto Individual ML_OPS

![](Henry.png)


## ETL
  
Realice un proyecto basado en un conjunto de datos donde teniamos 3 dataset en formato json, extraídos de la plataforma Steam Games.

Obteniendo los 3 dataset comenzamos desanidando las columnas que eran necesarias para obtener mas informacion y poder hacer un join entre las tablas,
luego en algunas columnas hicimos algunas transformaciones como el tipo de dato, eliminamos valores nulos donde era necesario para el rendimiento de la API y para que los endpoints funcionen correctamente. 

Por ultimo, se añadio una tabla de análisis de sentimiento que clasifica los comentarios en positivos, negativos y neutros mediante el uso de la librería NLTK. En esta tabla, los comentarios positivos se etiquetan con el número 2, los comentarios negativos con el número 0 y los comentarios neutros se etiquetan con el número 1.

## EDA (Analisis exploratorio de datos)

Realizamos un análisis exploratorio de datos después de completar la transformación y carga de datos (ETL). En primer lugar, obtuvimos una visión general de los años, examinamos las características de los precios, analizamos los comentarios y detectamos posibles valores duplicados.

Luego, procedimos a eliminar los valores duplicados al comparar múltiples columnas. La decisión de eliminarlos se basó en la observación de que, al hacerlo, no afectaría significativamente la integridad del dataset y calculamos la existencia de los posibles valores atipicos.

Finalmente, representamos gráficamente la distribución del análisis de sentimiento por año y trazamos la evolución de los comentarios positivos y negativos a lo largo del tiempo.

## Modelo de aprendizaje automático 

Desarrolle una función que nos permite seleccionar un juego y obtener cinco recomendaciones de juegos similares al elegido

## API

Se ha creado un entorno virtual y se han instalado todas las bibliotecas necesarias para desarrollar una API. Esta API consta de cinco funciones que realizan diferentes consultas, además se creo una función donde fue entrenada con machine learning que nos proporciona recomendaciones de juegos en función del juego especificado en la consulta.
