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