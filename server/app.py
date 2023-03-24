from flask import Flask
from flask_restx import Api, Resource, fields
from basic import Basic 
from chat import Chat

app = Flask(__name__)
api = Api(app, version='0.0.1', title='Sigongan AI',
    description='Sigongan AI API',
)

api.add_namespace(Basic, '/basic')
api.add_namespace(Chat, '/chat')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)