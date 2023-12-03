from flask import Blueprint
from flask import render_template
import mysql.connector


bp = Blueprint('main', __name__, url_prefix='/')

db_config = {
    'host': '192.168.56.101',
    'port': '4567',
    'user': 'root',
    'password': '1234',
    'database': 'term_project',
}


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/connect-db')
def connect_db():
    try:
        connection = mysql.connector.connect(**db_config)
        connection.close()
        return render_template('connect.html')
        
    except mysql.connector.Error as err:
        return f"Error: {err}"
