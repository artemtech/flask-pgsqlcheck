from flask import Flask, make_response
import psycopg2
import os

app = Flask(__name__)

db_configs = {
    "host": os.environ.get('POSTGRESQL_HOST', 'localhost'),
    "database": os.environ.get('POSTGRESQL_DB', 'postgres'),
    "user": os.environ.get('POSTGRESQL_USER', 'postgres'),
    "password": os.environ.get('POSTGRESQL_PASS', ''),
    "port": os.environ.get('POSTGRESQL_PORT', 5432),
}

def check_postgresql():
    conn = None
    recovery = None
    try:
        conn = psycopg2.connect(**db_configs)
        cur = conn.cursor()
        cur.execute("select pg_is_in_recovery()")

        recovery = cur.fetchone()[0]
        cur.close()
    except Exception as error:
        app.logger.debug(error)
    finally:
        if conn is not None:
            conn.close()
    return recovery

@app.route('/', methods=['GET'])
def pgsqlcheck():
    recovery = check_postgresql()
    if recovery == True:
        response = make_response("Standby", 206)
    elif recovery == False:
        response = make_response("Primary", 200)
    else:
        response = make_response("DBDown", 503)
    response.mimetype = "text/plain"
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=25432)
