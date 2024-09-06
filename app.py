from flask import Flask, jsonify, request, render_template
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Cargar el dataframe
df_games = pd.read_csv('df_games.csv')

@app.route("/")
def index():
    return render_template('index.html')

@app.get("/Developer")
def Developer():
    developer = request.args.get('developer', '')

    if developer:
        df_developer = df_games[df_games["developer"] == developer]
        # Calcular el total de aplicaciones por año
        cantidad_items = df_developer.groupby('release_date')['item_id_x'].count().reset_index()

        # Los que tienen precio lo instanciamos como "No Free"
        df_developer.loc[df_developer["price"].apply(lambda x: isinstance(x, float)), "price"] = "No Free"
        
        # Agrupamos por año y precios "Free" y "No Free"
        porcentaje = df_developer.groupby(["release_date", "price"])["price"].count().unstack()
        
        # Calcula el porcentaje de elementos "Free" por año
        if 'Free' in porcentaje.columns:
            if 'No Free' in porcentaje.columns:
                porcentaje["Porcentaje_Free"] = (porcentaje["Free"] / (porcentaje["Free"] + porcentaje["No Free"])) * 100
            else:
                porcentaje["Porcentaje_Free"] = (porcentaje["Free"] / porcentaje["Free"]) * 100
        else:
            porcentaje["Porcentaje_Free"] = 0
        
        porcentaje = porcentaje.fillna(0)
        
        años = df_developer.groupby('release_date')["item_id_x"].count().reset_index()
        
        porcentaje_free = list(porcentaje["Porcentaje_Free"].map("{:.2f}%".format))
        años = list(cantidad_items["release_date"])
        cantidad_items = list(cantidad_items["item_id_x"])

        # Hacemos un zip con las tres listas 
        listas_unidas = list(zip(años, cantidad_items, porcentaje_free))

        # Agregamos las claves para cada índice
        claves = ['Año', 'Cantidad', 'Porcentaje']
        diccionario = [dict(zip(claves, fila)) for fila in listas_unidas]

        return jsonify(diccionario)
    else:
        return jsonify({"error": "Desarrolladora no proporcionada"})

@app.get("/UserForGenre")
def UserForGenre():
    genero = request.args.get('genero', '')

    if genero:
        df_genero = df_games[df_games["genres"] == genero]
        df_agrupados = df_genero.groupby(["genres", "user_id"])["playtime_forever"].sum().reset_index()

        if not df_agrupados.empty:
            usuario_horas_jugadas = df_agrupados[df_agrupados["playtime_forever"] == df_agrupados["playtime_forever"].max()]["user_id"].values[0]
        else:
            usuario_horas_jugadas = None

        df_horas_acumulado = df_genero[df_genero["user_id"] == usuario_horas_jugadas]
        acumulacion_horas = df_horas_acumulado.groupby('release_date')['playtime_forever'].sum().cumsum()
        lista_horas = acumulacion_horas.tolist()

        acumulacion_años = df_horas_acumulado.groupby('release_date')['playtime_forever'].count().reset_index()
        lista_años = acumulacion_años["release_date"].tolist()

        data = {
            'Años': lista_años,
            'Horas': lista_horas
        }

        return jsonify(data)
    else:
        return jsonify({"error": "Género no proporcionado"})

@app.get("/Userdata")
def Userdata():
    user_id = request.args.get('User_id', '')

    if user_id:
        df_usuario = df_games[df_games["user_id"] == user_id]
        df_usuario['price'] = pd.to_numeric(df_usuario['price'], errors='coerce')
        dinero_gastado = df_usuario['price'].sum()
        porcentaje_recomendacion = df_usuario["recommend"].mean() * 100
        cantidad_items = df_usuario["item_id_x"].count()

        diccionario = {
            'Usuario': user_id,
            'Dinero gastado': f"{dinero_gastado} USD",
            '% de recomendación': f"{porcentaje_recomendacion:.2f}%",
            'Cantidad de items': cantidad_items
        }

        return jsonify(diccionario)
    else:
        return jsonify({"error": "ID de usuario no proporcionado"})

@app.get("/Best_developer_year")
def Best_developer_year():
    año = request.args.get('año', type=int)

    if año:
        df_desarrolador = df_games[df_games["release_date"] == año]
        df_agrupados = df_desarrolador.groupby(["developer"])["recommend"].sum().reset_index()
        juego_mas_recomendado = df_agrupados.sort_values(by='recommend', ascending=False).head(3)

        data = {
            'Puesto 1': juego_mas_recomendado.iloc[0]["developer"],
            'Puesto 2': juego_mas_recomendado.iloc[1]["developer"],
            'Puesto 3': juego_mas_recomendado.iloc[2]["developer"]
        }

        return jsonify(data)
    else:
        return jsonify({"error": "Año no proporcionado"})

@app.get("/Developer_reviews_analysis")
def developer_reviews_analysis():
    desarrolladora = request.args.get('desarrolladora', '')

    if desarrolladora:
        df_desarrolador = df_games[df_games["developer"] == desarrolladora]
        cantidad_registros = df_desarrolador["sentiment_analysis"].value_counts().reset_index()
        positivos = f"Positivos = {cantidad_registros.iloc[0][1]}" if len(cantidad_registros) > 0 else "Positivos = 0"
        negativos = f"Negativos = {cantidad_registros.iloc[2][1]}" if len(cantidad_registros) > 2 else "Negativos = 0"
        data = {
            desarrolladora: [positivos, negativos]
        }
    else:
        data = {"error": "Desarrolladora no proporcionada"}

    return jsonify(data)

@app.post("/Recomendacion_juego")
def Recomendacion_juego():
    item_name = request.form.get('item_name', '')

    if item_name:
        user_item_matrix = pd.pivot_table(df_games, values='playtime_forever', index='user_id', columns='item_name', fill_value=0)
        game_similarity = cosine_similarity(user_item_matrix.T)

        if item_name in user_item_matrix.columns:
            game_index = user_item_matrix.columns.get_loc(item_name)
            game_similarities = game_similarity[game_index]

            similar_games = pd.DataFrame({
                'Game': user_item_matrix.columns,
                'Similarity': game_similarities
            })

            top_n_recommendations = similar_games.sort_values(by='Similarity', ascending=False).head(6)
            top_n_recommendations = dict(top_n_recommendations["Game"][1:])  # Exclude the item itself
        else:
            top_n_recommendations = {"error": "Juego no encontrado"}

        return jsonify(top_n_recommendations)
    else:
        return jsonify({"error": "Nombre del juego no proporcionado"})

if __name__ == '__main__':
    app.run(debug=True)

