import os
from flask import Flask, jsonify, request
import psycopg2
import redis
from time import sleep

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def wait_for_db(max_retries=20):
    for _ in range(max_retries):
        try:
            conn = get_conn()
            conn.close()
            return
        except Exception:
            sleep(1)

    raise RuntimeError('La base de datos no responde ＞﹏＜')

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.get('/')
def home():
    r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    r.incr('visits')
    
    return jsonify({
        'msg': "Hola desde Docker Compose!",
        'services': {
            '/health' : "Verifica la salud de la aplicación",
            '/visits' : "Cuenta las visitas usando redis"
        }
    }), 200
 
 
@app.get('/health')
def health():
  try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    now = cur.fetchone()[0]
    cur.close()
    
    # Verificar Redis
    r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    pong = r.ping()
    
    return jsonify({
        'status': 'ok', 
        'database_time': str(now),
        'redis_ping': pong
    }), 200
  
  except Exception as e:
      return jsonify({
        'status': 'error', 
        'msg': str(e)}), 500
 
 
@app.get('/visits')
def visits():
    try:
        r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
        count = r.incr('visits')
        return jsonify({'visits': int(count)}), 200

    except Exception as e:
        return jsonify({
            'msg': "error",
            'error': str(e)
        }), 500
    

# --- Endpoints de User ---
@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = get_conn()
    cur = conn.cursor()
    
    r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    r.incr('visits')

    if request.method == 'GET':
        cur.execute("SELECT id, nombre, apellido FROM users ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'id': r[0], 'nombre': r[1], 'apellido': r[2]} for r in rows]), 200

    elif request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')
        apellido = data.get('apellido')

        if not nombre or not apellido:
            return jsonify({'error': 'nombre y apellido son requeridos'}), 400

        cur.execute(
            "INSERT INTO users (nombre, apellido) VALUES (%s, %s) RETURNING id;",
            (nombre, apellido)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': new_id, 'nombre': nombre, 'apellido': apellido}), 201


    
if __name__ == '__main__':
    wait_for_db()
    init_db()
    app.run(host='0.0.0.0', port=8000)
    