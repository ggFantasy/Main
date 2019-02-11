from flask import Flask
from flask_restful import Api

from ggfantasy.hapi.endpoints.match_details import MatchDetails

app = Flask(__name__)
api = Api(app)

api.add_resource(MatchDetails, '/v1/MatchDetails', '/v1/MatchDetails/')


if __name__ == '__main__':
    app.run(debug=True)