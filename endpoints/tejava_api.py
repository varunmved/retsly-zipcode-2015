from flask import *
from utils.mysqlconn import MySQLDBConn
from models.tejava_sauce import buildpolygon, polylistings


api_blueprint = Blueprint("tejava_api", __name__)

@api_blueprint.route("/testresults")
def test_results():
    code = 200
    polygon = buildpolygon(37.788889, -122.399864, 10, 4)
    results = polylistings(polygon)
    
    if "error" in results:
        code = 500
    
    return jsonify(results), code

@api_blueprint.route("/polylistings/<float:latitude>/<float:longitude>/<int:max_minutes>")
def listings(latitude, longitude, max_minutes):
    code = 200
    # TODO: ignore endpoint params right now
    polygon = buildpolygon(37.788889, -122.399864, 4)
    results = polylistings(polygon)

    if "error" in results: code = 500
    return jsonify(results), code

