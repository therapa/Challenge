import sqlite3, json
import time
from flask import Flask, request, jsonify, url_for
from flask_restful import Resource, Api
from sqlalchemy import create_engine

# Conexion a la bd
db_connect = create_engine('sqlite:///db.db')



app = Flask(__name__)
api = Api(app)

# Ruta Raiz
@app.route('/')
def api_root():
	return 'Bienvenido a la API para centralizar los resultados de los scripts 		ejecutados en Debian'


servidores = []
# Ruta de consulta de servidores cargados
@app.route('/servidores', methods=["GET"])
def getServidores():
        return jsonify(servidores)
# Ruta de consulta de servidores cargados por Nro
@app.route('/servidor/<id>', methods=["GET"])
def getServidor(id):
	id = int(id) -1
	return jsonify(servidores[id])

# Ruta de consulta de servidores cargados en bd
@app.route('/bd', methods=["GET"])
def getbd():
        conn = db_connect.connect()
        query = conn.execute("select * from Servidores;")
        Ser = {'Servidores': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(Ser)


# Endpoint de consulta POST para cargar servidores
@app.route('/servidor', methods=["POST"])
def addServidor():
	    
    	request.get_data()
    	request.is_json
    	content = request.get_json()
	servidores.append(content)
        conn = db_connect.connect()
        CPUMODEL = content['CPUMODEL']
	CPUCORES = content['CPUCORES']
        DATE = content['DATE']
        IP = content['IP']
        SESSION = content['SESSION']
        SO = content['SO'] 
        VERSION = content['VERSION'] 
        query2 = conn.execute("insert into Servidores values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(CPUMODEL, CPUCORES, DATE, IP, SESSION, SO, VERSION))
        IPS = content['IP']
        hoy = time.strftime("%Y-%m-%d")
        IPS = IP[:-3]+"_"+hoy+".json"
   	with open(IPS, 'w') as file:
        	datosdump = json.dump(content, file, indent=4)
        return jsonify(content)
        
if __name__ == '__main__':
    app.run(port='5000')



