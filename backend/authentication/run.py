import os
from app import create_app

env = os.getenv('FLASK_ENV', 'development')

app = create_app(env=env)

if __name__ == "__main__":
    app.run()
