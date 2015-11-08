import json as json
from flask import *
from utils.mysqlconn import MySQLDBConn
from models.tejava_sauce import buildpolygon, polylistings, populatepolygon


api_blueprint = Blueprint("tejava_api", __name__)

@api_blueprint.route("/testresults")
def test_results():
    code = 200
    polygon = buildpolygon(33.4388326,-112.0262216, 45, 16)
    results = polylistings(polygon)
    
    if "error" in results:
        code = 500
    
    return jsonify(results), code

@api_blueprint.route("/pagepolylistings")
def pagelistings():
    params = request.args
    offset = int(params["offset"])
    limit = int(params["limit"])
    polygon_str = params["polygon"]
    # polygon_str = request.get_data(as_text=True)
    polygon_data = json.loads(polygon_str)
    
    code = 200
    polygon = populatepolygon(polygon_data)
    results = polylistings(polygon, offset=offset, limit=limit)

    if "error" in results: code = 500
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

