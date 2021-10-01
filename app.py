import os
from config import ConfigNames
from src import create_app, db
from flask_migrate import Migrate
from werkzeug.utils import redirect
from http import HTTPStatus


app = create_app(ConfigNames.from_str(os.getenv('CONFIG_TYPE', 'DEVELOPMENT')))


from src.models.product import Product
from src.models.user import User


migrate = Migrate(app, db)


@app.route("/")
def index():
    return redirect("/swagger-ui"), HTTPStatus.PERMANENT_REDIRECT


if __name__ == "__main__":
    app.run(debug=True)
