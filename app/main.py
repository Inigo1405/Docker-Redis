# pyright: reportMissingImports=false

import os
from flask import Flask, jsonify
import psycopg2
import redis
from time import sleep

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')

def wait_for_db(max_retries=20):
	for _ in range(max_retries):
		try:
			conn = psycopg2.connect(DATABASE_URL)
			conn.close()
			return
		except Exception:
			sleep(1)
    
	raise RuntimeError('La base de datos no responde ＞﹏＜')


@app.get('/')
def home():
	return jsonify({
		'msg': "Hola desde Docker Compose!",
		'services': {
			'/health' : "Verifica la salud de la aplicación",
			'/visits' : "Cuenta las visitas usando redis"
		}
	})
 
 
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
    }), 500
  
  except Exception as e:
      return jsonify({
        'status': 'error', 
        'msg': str(e)}), 500
 
 
@app.get('/visits')
def visits():
    try:
        r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
        count = r.incr('visits')
        return jsonify({'visits': int(count)})

    except Exception as e:
        return jsonify({
            'msg': "error",
            'error': str(e)
        }), 500
    
    
    
if __name__ == '__main__':
    wait_for_db()
    app.run(host='0.0.0.0', port=8000)
    