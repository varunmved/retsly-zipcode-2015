from flask import *
from utils.mysqlconn import MySQLDBConn
from models.tejava_sauce import buildpolygon, polylistings


api_blueprint = Blueprint("tejava_api", __name__)

@api_blueprint.route("/testresults")
def test_results():
    code = 200
    # cow palace
    polygon = buildpolygon(37.7068324,-122.4209305, 10, 4)
    results = polylistings(polygon)
    
    if "error" in results:
        code = 500
    
    return jsonify(results), code


@api_blueprint.route("/polylistings")
def listings():
    params = request.args
    latitude = float(params["latitude"])
    longitude = float(params["longitude"])
    max_minutes = int(params["max_minutes"])

    code = 200
    polygon = buildpolygon(latitude, longitude, max_minutes, precision=12)
    results = polylistings(polygon)

    if "error" in results: code = 500
    return jsonify(results), code

