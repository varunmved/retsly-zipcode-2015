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

    return polygon


def polylistings(polygon):
    """uses the retsly API to return a list of properties that fall within the defined polygon"""

    vendorID = "test_sf"
    resource = "listings"
    token = os.getenv("RETSLY_TOKEN", "notatoken")

    try:
        # flatten the list of dicts into a list

        #list of dicts to list of lists
        points = [(str(vertex.long), str(vertex.lat)) for vertex in polygon.points]
        
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
                "polygon": polygon.vertices(),
                "listings": listings,
                "n_results": len(listings),
            }
        else:
            return response.text


        return data
    except Exception as e:
        print(str(e))
        return {"error": str(e)}
