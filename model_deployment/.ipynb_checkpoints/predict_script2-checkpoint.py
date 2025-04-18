import pandas as pd
import joblib
import os

def predict_popularity(features_list):
    """
    Predice la popularidad de una canción en base a sus características.

    features_list: lista o array con 14 valores en el siguiente orden:
    ['duration_ms', 'explicit', 'danceability', 'energy', 'key', 'loudness',
     'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
     'valence', 'tempo', 'time_signature']
    """
    # Cargar el modelo
    model = joblib.load(os.path.dirname(__file__) + '/rf.pkl')
    
    column_names = [
        'duration_ms', 'explicit', 'danceability', 'energy', 'key', 'loudness',
        'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
        'valence', 'tempo', 'time_signature'
    ]

    # Crear dataframe con una sola fila
    input_df = pd.DataFrame([features_list], columns=column_names)

    # Predecir la popularidad
    popularity = model.predict(input_df)[0]

    return popularity
