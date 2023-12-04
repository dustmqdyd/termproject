from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
import mysql.connector


bp = Blueprint('main', __name__, url_prefix='/')

db_config = {
    'host': '192.168.56.101',
    'port': '4567',
    'user': 'root',
    'password': '1234',
    'database': 'term_project',
}


global connection

def get_database_connection():
    return mysql.connector.connect(**db_config)

def close_database_connection(connection):
    if connection and connection.is_connected():
        connection.close()

def execute_query(query):
    global connection
    cursor = connection.cursor()
    cursor.execute(query)
    data_list = cursor.fetchall()
    cursor.close()
    return data_list


def insert_sim_query(sid, s_type, status, phone):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = "INSERT INTO SIM (sid, type, status, phone_number) VALUES (%s, %s, %s, %s)"
        data = (sid, s_type, status, phone)

        cursor.execute(query, data)
        connection.commit()
        print('hi')
        return True  # Insertion successful

    except mysql.connector.Error as err:
        print(f"Error inserting user: {err}")
        return False  # Insertion failed

    finally:
        if cursor:
            cursor.close()
        close_database_connection(connection)


def insert_user_query(uid, name, birth_date, sim_sid):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = "INSERT INTO USER (uid, name, birth_date, ssid) VALUES (%s, %s, %s, %s)"
        data = (uid, name, birth_date, sim_sid)

        cursor.execute(query, data)
        connection.commit()

        return True

    except mysql.connector.Error as err:
        print(f"Error inserting user: {err}")
        return False

    finally:
        if cursor:
            cursor.close()
        close_database_connection(connection)


def insert_price_query(plan_name, bill, data_limit, call_limit):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = "INSERT INTO PRICE (plan_name, bill, data_limit, call_limit) VALUES (%s, %s, %s, %s)"
        data = (plan_name, bill, data_limit, call_limit)

        cursor.execute(query, data)
        connection.commit()

        return True

    except mysql.connector.Error as err:
        print(f"Error inserting user: {err}")
        return False

    finally:
        if cursor:
            cursor.close()
        close_database_connection(connection)


def insert_plan_query(plan_id, pname, mgr_sid):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = "INSERT INTO PRICE (plan_id, pname, mgr_sid) VALUES (%s, %s, %s)"
        data = (plan_id, pname, mgr_sid)

        cursor.execute(query, data)
        connection.commit()

        return True

    except mysql.connector.Error as err:
        print(f"Error inserting user: {err}")
        return False

    finally:
        if cursor:
            cursor.close()
        close_database_connection(connection)



def insert_payment_query(card_id, cvc, company, payment_date, mgr_uid):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = "INSERT INTO PRICE (card_id, cvc, company, payment_date, mgr_uid) VALUES (%s, %s, %s, %s, %s)"
        data = (card_id, cvc, company, payment_date, mgr_uid)

        cursor.execute(query, data)
        connection.commit()

        return True

    except mysql.connector.Error as err:
        print(f"Error inserting user: {err}")
        return False

    finally:
        if cursor:
            cursor.close()
        close_database_connection(connection)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/connect-db')
def connect_db():
    try:
        global connection
        connection = mysql.connector.connect(**db_config)
        return render_template('connect.html')
        
    except mysql.connector.Error as err:
        return f"Error: {err}"
    

@bp.route('/table/<table_name>')
def table(table_name):
    try:
        query = f'SELECT * FROM {table_name};'
        result = execute_query(query)
        return render_template('table.html', table_name=table_name, data=result)
    except Exception as err:
        return f"Error: {err}"


@bp.route('/insert-sim', methods=['POST'])
def insert_sim():
    if request.method == 'POST':
        # Extract form data
        sid = request.form.get('sid')
        s_type = request.form.get('s_type')
        status = request.form.get('status')
        phone = request.form.get('phone')

        if insert_sim_query(sid, s_type, status, phone):
            return render_template('insert_sim.html', sid=sid, s_type=s_type, status=status, phone=phone)
        else:
            flash({'error': 'Error inserting user. Please try again.'})


@bp.route('/insert-user', methods=['POST'])
def insert_user():
    if request.method == 'POST':
        # Extract form data
        uid = request.form.get('uid')
        name = request.form.get('user_name')
        birth_date = request.form.get('birth_date')
        sim_sid = request.form.get('sim_sid')

        if insert_user_query(uid, name, birth_date, sim_sid):
            return render_template('insert_user.html', uid=uid)
        else:
            flash({'error': 'Error inserting user. Please try again.'})


@bp.route('/insert-price', methods=['POST'])
def insert_price():
    if request.method == 'POST':
        # Extract form data
        plan_name = request.form.get('plan-name')
        bill = request.form.get('bill')
        data_limit = request.form.get('data_limit')
        call_limit = request.form.get('call_limit')

        if insert_price_query(plan_name, bill, data_limit, call_limit):
            return render_template('insert_price.html')
        else:
            flash({'error': 'Error inserting user. Please try again.'})


@bp.route('/insert-plan', methods=['POST'])
def insert_plan():
    if request.method == 'POST':
        # Extract form data
        plan_id = request.form.get('plan-id')
        pname = request.form.get('pname')
        mgr_sid = request.form.get('mgr_sid')

        if insert_plan_query(plan_id, pname, mgr_sid):
            return render_template('insert_user.html')
        else:
            flash({'error': 'Error inserting user. Please try again.'})


@bp.route('/insert-payment', methods=['POST'])
def insert_payment():
    if request.method == 'POST':
        # Extract form data
        card_id = request.form.get('card_id')
        cvc = request.form.get('cvc')
        company = request.form.get('company')
        payment_date = request.form.get('payment_date')
        mgr_uid = request.form.get('mgr_uid')

        if insert_payment_query(card_id, cvc, company, payment_date, mgr_uid):
            return render_template('insert_user.html')
        else:
            flash({'error': 'Error inserting user. Please try again.'})