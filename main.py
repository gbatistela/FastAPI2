from fastapi import FastAPI

app = FastAPI()


# Obtenemos el dataframe
import pandas as pd
df_games = pd.read_csv("C:\\Users\\Giuliano\\Desktop\\PI MLOps - STEAM\\df_games.csv")

@app.get("/Developer")
def Developer(developer:str):

    df_developer = df_games[df_games["developer"] == developer]
    # Calcular el total de aplicaciones por año
    Cantidad_Items = df_developer.groupby('release_date')['item_id_x'].count().reset_index()


    # Los que tienen precio lo instanciamos como "No Free"
    df_developer.loc[df_developer["price"].apply(lambda x: isinstance(x, float)), "price"] = "No Free"
    # Agrupamos por año y precios "Free" y "No Free"
    Porcentaje = df_developer.groupby(["release_date", "price"])["price"].count().unstack().fillna(0)
    # Calcula el porcentaje de elementos "Free" por año
    Porcentaje["Porcentaje_Free"] = (Porcentaje["Free"] / (Porcentaje["Free"] + Porcentaje["No Free"])) * 100

    Años = df_developer.groupby('release_date')["item_id_x"].count().reset_index()

    Porcentaje_Free = list(Porcentaje["Porcentaje_Free"].map("{:.2f}%".format))
    Años = list(Cantidad_Items["release_date"])
    Cantidad_Items = list(Cantidad_Items["item_id_x"])

    # Hacemos un zip con las tres listas 
    listas_unidas = list(zip(Años,Cantidad_Items, Porcentaje_Free))

    # Agregamos las claves para cada indice
    claves = ['Año', 'Cantidad', 'Porcentaje']
    diccionario = [dict(zip(claves, fila)) for fila in listas_unidas]

    return diccionario


@app.get("/UserForGenre")
def UserForGenre(genero):

  # Hacemos un dataframe con el genero que le indicamos en la funcion
  df_genero = df_games[df_games["genres"]== genero]

  # Agrupamos por Usuario el dataframe df_genero
  df_agrupados = df_genero.groupby(["genres","user_id"])["playtime_forever"].sum().reset_index()

  # Usuario que acumulo mas horas jugadas para el genero dado
  if not df_agrupados.empty:
    Usuario_Horas_Jugadas = df_agrupados[df_agrupados["playtime_forever"]== df_agrupados["playtime_forever"].max()]["user_id"].values[0]
  else:
    Usuario_Horas_Jugadas = None
  # LISTA ACUMULADA POR AÑO
  # Hacemos un dataframe para el usuario que mas horas jugo con sus años ordenados
  df_Horas_Acumulado = df_genero.sort_values(by='release_date')
  df_Horas_Acumulado = df_genero[df_genero["user_id"] == Usuario_Horas_Jugadas]

  # Calculamos la horas y años de acumulacion y hacemos una lista
  Acumulacion_Horas = df_Horas_Acumulado.groupby('release_date')['playtime_forever'].sum().cumsum()
  Lista_Horas = Acumulacion_Horas.tolist()

  Acumulacion_Años = df_Horas_Acumulado.groupby('release_date')['playtime_forever'].count().reset_index()
  Lista_Años = Acumulacion_Años["release_date"].tolist()

  # Crear un diccionario que contenga las dos listas
  data = {
    'Años': Lista_Años,
    'Horas': Lista_Horas
    }

  return f"Usuario con más horas jugadas para genero: {data}"



@app.get("/Userdata")
def Userdata(User_id : str):
    
    # Agrupamos por usuario
    df_usuario = df_games[df_games["user_id"]== "DrMolo"]

    # Convertir los valores de la columna a números (omitir los strings)
    df_usuario['price'] = pd.to_numeric(df_usuario['price'], errors='coerce')
    # Sumamos el dinero total gastado del usuario
    df_dinero_gastado = df_usuario['price'].sum()

    # Obtenemos el porcentaje de recomendacion
    Porcentaje_Recomendacion = df_usuario["recommend"].mean() * 100
    Porcentaje_Recomendacion

    Cantidad_items = df_usuario["item_id_x"].count()
    
    #{"Usuario X" : us213ndjss09sdf, "Dinero gastado": 200 USD, "% de recomendación": 20%, "cantidad de items": 5}
    diccionario = f"Usuario X: {User_id}, Dinero gastado: {df_dinero_gastado} USD, % de recomendación: {Porcentaje_Recomendacion}%, Cantidad de items: {Cantidad_items} "
            
    
    return diccionario

@app.get("/Best_developer_year")
def Best_developer_year(año:int):

    
    df_desarrolador = df_games[df_games["release_date"] == año]
    # Agrupamos por desarrolador y sumamos las remcomendaciones 
    df_agrupados = df_desarrolador.groupby(["developer"])["recommend"].sum().reset_index()
    # Ordenamos los top 3 desarroladores mas recomendados
    Juego_mas_recomendado = df_agrupados.sort_values(by='recommend', ascending=False).head(3)

    data = {
            'Puesto 1': Juego_mas_recomendado.iloc[0]["developer"],
            'Puesto 2': Juego_mas_recomendado.iloc[1]["developer"],
            'Puesto 3': Juego_mas_recomendado.iloc[2]["developer"]
        }

    return data

@app.get("/developer_reviews_analysis")
def developer_reviews_analysis( desarrolladora : str ):

    df_desarrolador = df_games[df_games["developer"] == desarrolladora]

    Cantidad_Registros = df_desarrolador["sentiment_analysis"].value_counts().reset_index()

    positivos = f"Positivos = {Cantidad_Registros.iloc[0][1]}"
    negativos =  f"Negativos = {Cantidad_Registros.iloc[2][1]}"
    usuario = desarrolladora
    data = {
                usuario:[positivos, negativos]
                }

    return data