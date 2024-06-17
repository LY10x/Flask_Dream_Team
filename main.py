from flask import Flask # type: ignore
from flask_restful import Api, Resource # type: ignore


app = Flask(__name__)
api = Api(app)

if __name__ == "__main__":
    app.run(debug=True)

