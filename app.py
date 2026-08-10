from flask import Flask, g, escape, session, redirect, render_template, request, jsonify, Response
from Misc.functions import ago
from Models.DAO import DAO as DAOClass

app = Flask(__name__)
app.secret_key = '#$ab9&^BB00_.'

# Initialize the database layer before creating the route blueprints.
DAO = DAOClass(app)

# Route modules are factories. This avoids importing app.py from inside a route,
# which was the cause of the circular-import crash.
from routes.user import create_user_blueprint
from routes.book import create_book_blueprint
from routes.admin import create_admin_blueprint

app.jinja_env.globals.update(
    ago=ago,
    str=str,
)

app.register_blueprint(create_user_blueprint(DAO))
app.register_blueprint(create_book_blueprint(DAO))
app.register_blueprint(create_admin_blueprint(DAO))


@app.get('/health')
def health():
    return {'status': 'ok'}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
