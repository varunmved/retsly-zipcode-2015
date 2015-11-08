import os
import requests
import json
import numpy

from utils.travelpolygon import TravelPolygon

def buildpolygon(latitude, longitude, max_minutes, precision=50):
    """estimate a polygon such that every point within the polygon is within
    max_minutes of the specified center (lat, long). precision defines the number
    of vertices to build the polygon

    latitude, longitude -- self explanatory
    max_minutes         -- max travel time from the specified lat long
    precision[optional] -- number of points used to estimate the polygon

    returns: list of dicts containing final lat, long. order of points matter
    """

    #TODO: actual code to calculate the polygon. return a hard-coded list for now
    polygon = TravelPolygon(latitude, longitude, max_minutes, precision)
    polygon.fit()

    polygon = [
        {"longitude": -122.455330, "latitude": 37.748186},
        {"longitude": -122.462540, "latitude": 37.736512},
        {"longitude": -122.456017, "latitude": 37.726194},
        {"longitude": -122.435417, "latitude": 37.713159},
        {"longitude": -122.414131, "latitude": 37.722392},
        {"longitude": -122.401428, "latitude": 37.728910},
        {"longitude": -122.402802, "latitude": 37.743571},
        {"longitude": -122.418594, "latitude": 37.757959},
        {"longitude": -122.410011, "latitude": 37.763930},
        {"longitude": -122.424431, "latitude": 37.770172},
        {"longitude": -122.430267, "latitude": 37.756058},
        {"longitude": -122.447433, "latitude": 37.759859},
        {"longitude": -122.455330, "latitude": 37.748186}]

    return polygon


def polylistings(polygon):
    """uses the retsly API to return a list of properties that fall within the defined polygon"""

    vendorID = "test_sf"
    resource = "listings"
    token = os.getenv("RETSLY_TOKEN", "notatoken")

    try:
        # flatten the list of dicts into a list

        #list of dicts to list of lists
        points = [(str(vertex["longitude"]), str(vertex["latitude"])) for vertex in polygon]

        # list of lists to list: http://stackoverflow.com/questions/10632839/python-transform-list-of-tuples-in-to-1-flat-list-or-1-matrix
        polypoints = list(sum(points, ()))
        polypoints = ",".join(polypoints)

        url =  "https://rets.io/api/v1/%s/%s" % (vendorID, resource)
        params = {
            "access_token": token,
            "poly": polypoints,
            # "bedrooms[gt]": 0,
            # "type": "Residential",
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            listings = []
            result = response.json()
            if "status" in result and result["status"] == 200:
                listings = result["bundle"]
            data = {
                "polygon": polygon,
                "listings": listings,
                "n_results": len(listings),
            }
        else:
            return response.text


        return data
    except Exception as e:
        print(str(e))
        return {"error": str(e)}
