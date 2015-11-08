import os
import math as math
import googlemaps
import datetime as datetime
import pdb


token = os.getenv("GOOGLE_TOKEN", "notatoken")
#print(token)
gmaps = googlemaps.Client(key=token)

class Point:
    """points are represented using polar coordinates"""

    def __init__(self, r, theta, start_long, start_lat):
        # lower, current, and upper values for the radius r
        self.lower_r = 0
        self.r = r
        self.prev_r = r
        self.upper_r = None

        self.theta = math.radians(theta)
        self.done = False
        self.long = start_long
        self.lat = start_lat
        self.update()

    def update(self):
        self.long = self.long + (self.r * math.cos(self.theta))
        self.lat = self.lat + (self.r * math.sin(self.theta))

    def __str__(self):
        a = "lat: %s, long: %s, r: %s, theta: %s" % (self.lat, self.long, self.r, self.theta)
        return a


class TravelPolygon:
    def __init__(self):
        self.points = []
        pass

    def populate(self, vertices):
        """create a polygon from a predefined list, of dicts, of latlongs"""
        for vertex in vertices:
            point = Point(0, 0, vertex["longitude"], vertex["latitude"])
            self.points.append(point)


    def build(self, latitude, longitude, max_time, slices):
        """create a polygon from scratch given a center and max travel time"""
        self.slices = slices
        self.max_time = max_time * 60   # convert minutes to seconds
        self.centerLat = latitude
        self.centerLong = longitude
        r_init = 1.0/69 # 1 mile ish
        for theta in range(0, 360, 360/slices):
            point = Point(r_init, theta, longitude,latitude)
            self.points.append(point)


    def __str__(self):
        s = ""
        for point in self.points:
            s += "%s, %s\n" % (point.lat, point.long)
        return s

    def vertices(self):
        vertices = []
        for point in self.points:
            vertex = {"longitude": point.long, "latitude": point.lat}
            vertices.append(vertex)
        return vertices

    def fit(self):
        alldone = False
        limit = 20
        i = 0
        tmode = "driving"

        depart = datetime.datetime(2015,11,10,7,0,0)
        while not alldone and i < limit:
            alldone = True
            i += 1
            print("------ iteration: %s" % i)
            try:
                # go through all the points and make 1 distance matrix request for all of
                # them
                startLatLong = str(self.centerLat)+ ',' + str(self.centerLong)
                polyLatLongs = "|".join([",".join([str(point.lat), str(point.long)]) for point in self.points])

                # start points, dest point
                response = gmaps.distance_matrix(polyLatLongs, startLatLong
                        , mode = tmode
                        , departure_time = depart)

                if "status" in response and response["status"] == "OK":
                    # all distances are in the rows key, listed in the order the cordinates were given
                    for j in range(0, len(response["rows"])):
                        result = response["rows"][j]
                        point = self.points[j]

                        if not point.done:
                            if result["elements"][0]["status"] == "ZERO_RESULTS":
                                point.r = point.prev_r
                                point.update()
                                point.done = True
                                continue
                            
                            if tmode == "driving":
                                travelTime = result['elements'][0]['duration_in_traffic']['value']
                            else:
                                travelTime = result['elements'][0]['duration']['value']

                            # how far off the point is from the desired distance. we'll accept 10% error
                            # print("max time: %s, travel_time: %s" % (self.max_time, travelTime))
                            dist_error = (1.0 * abs(self.max_time - travelTime))/self.max_time
                            # print("theta: %s, %s -- %s, %s" % (point.theta, self.max_time, travelTime, dist_error))

                            if (dist_error <= .4 and travelTime < self.max_time) or\
                                    dist_error <= .15:
                                point.done = True
                            elif (travelTime > self.max_time):
                                point.upper_r = point.r
                                self.prev_r = point.r
                                point.r = (point.r ) / 2.0
                                point.update()
                            elif(travelTime < self.max_time):
                                point.lower_r = point.r
                                point.prev_r = point.r
                                if point.upper_r is None:
                                    # point.r +=  (2/69.0) # add 10 miles ish
                                    point.r *= 1.25
                                else:
                                    point.r = (point.r + point.upper_r) / 2.0
                                point.update()

                        alldone = alldone and point.done
                else:
                    print("distance matrix failed")
                    pdb.set_trace()
                    break


            except Exception as e:
                print(e)
                pdb.set_trace()

# Lumo Offices: 37.4256015,-122.1459576
# zip.Code: 37.788894,-122.4002976
# phoenix airport: 33.4388326,-112.0262216
# a

# shape = TravelPolygon()
# shape.build(33.4388326,-112.0262216, 30, 16)
# shape.fit()
# print(shape)
