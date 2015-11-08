from flask import *
from utils.mysqlconn import MySQLDBConn
from models.tejava_sauce import buildpolygon, polylistings


api_blueprint = Blueprint("tejava_api", __name__)

@api_blueprint.route("/testresults")
def test_results():
    code = 200
    polygon = buildpolygon(0, 0, 10)
    results = polylistings(polygon)
    
    if "error" in results:
        code = 500
    
    return jsonify(results), code
