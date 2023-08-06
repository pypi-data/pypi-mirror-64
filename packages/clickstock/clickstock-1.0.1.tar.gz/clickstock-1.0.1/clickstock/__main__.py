import os
import sys
import connexion
from flask_pymongo import PyMongo


def create_app():
    app = connexion.FlaskApp(__name__,
                             specification_dir='openapi/')
    app.add_api('my_api.yml')

    return app


def main():
    app = create_app()
    app.run(port=8080)


if __name__ == '__main__':
    sys.exit(main())
