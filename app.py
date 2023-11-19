from flask import Flask

app = Flask(__name__)


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    return app
