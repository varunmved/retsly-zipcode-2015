from flask import *
from utils.mysqlconn import MySQLDBConn


api_blueprint = Blueprint("caltrain_api", __name__)

@api_blueprint.route("/random/<int:value>")
def random_station(value):
    station = {}

    with MySQLDBConn() as db_conn:
        results = db_conn.executeReadQueryHash("select * from stops")
        idx = value % len(results)
    
    return jsonify(results[idx])


