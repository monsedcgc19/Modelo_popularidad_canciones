from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
import joblib
import sys
import os

# Añadir ruta a la carpeta del modelo
sys.path.append(os.path.abspath('model_deployment'))
from predict_script2 import predict_popularity

app = Flask(__name__)

api = Api(
    app, 
    version='1.0', 
    title='Popularidad de Canciones API',
    description='Predice la popularidad de una canción a partir de sus características.'
)

ns = api.namespace('predict', description='Predicción de popularidad')

# Parser para recibir los 14 parámetros
parser = reqparse.RequestParser()
parser.add_argument('duration_ms', type=float, required=True)
parser.add_argument('explicit', type=int, required=True)
parser.add_argument('danceability', type=float, required=True)
parser.add_argument('energy', type=float, required=True)
parser.add_argument('key', type=int, required=True)
parser.add_argument('loudness', type=float, required=True)
parser.add_argument('mode', type=int, required=True)
parser.add_argument('speechiness', type=float, required=True)
parser.add_argument('acousticness', type=float, required=True)
parser.add_argument('instrumentalness', type=float, required=True)
parser.add_argument('liveness', type=float, required=True)
parser.add_argument('valence', type=float, required=True)
parser.add_argument('tempo', type=float, required=True)
parser.add_argument('time_signature', type=int, required=True)

resource_fields = api.model('Prediction', {
    'predicted_popularity': fields.Float,
})

@ns.route('/')
class PopularityApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        input_values = [
            args['duration_ms'], args['explicit'], args['danceability'], args['energy'],
            args['key'], args['loudness'], args['mode'], args['speechiness'],
            args['acousticness'], args['instrumentalness'], args['liveness'],
            args['valence'], args['tempo'], args['time_signature']
        ]
        prediction = predict_popularity(input_values)
        return { 'predicted_popularity': prediction }, 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
