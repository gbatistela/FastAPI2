from fastapi import FastAPI

app = FastAPI()


# Obtenemos el dataframe
import pandas as pd
df_games = pd.read_csv("df_games.csv")

@app.get("/Developer")
def Developer(developer:str):

    df_developer = df_games[df_games["developer"] == developer]
    # Calcular el total de aplicaciones por año
    Total_Por_Año = df_developer.groupby('release_date')['price'].count()
    
    # Calcular el porcentaje de aplicaciones "Free" por año
    Porcentaje_Free = (df_developer[df_developer['price'] == 'Free'].groupby('release_date')['price'].count() / Total_Por_Año) * 100

    # Crear un DataFrame de resumen
    # Crear un DataFrame de resumen
    df = pd.DataFrame({
       'Cantidad Items': Total_Por_Año,
        'Contenido Free': Porcentaje_Free
        
    })
    
    return df


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
      
  


  return f"Usuario con más horas jugadas para {genero}: {data}"