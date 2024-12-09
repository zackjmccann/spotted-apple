import os
from src import create_app
from distutils.util import strtobool


app = create_app()

if __name__ == "__main__":
    debug = bool(strtobool(os.getenv('FLASK_DEBUG', 'false')))
    app.run(debug=debug)
