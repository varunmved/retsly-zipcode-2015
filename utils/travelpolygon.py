import math as math

NUM_OF_SLICES = 50

pointsList = []

class Point:
    def __init__(self, r, theta, start_long, start_lat):
        self.r = r
        self.theta = math.radians(theta)
        self.long = start_long + (r * math.cos(self.theta))
        self.lat = start_lat + (r * math.sin(self.theta))
        self.done = False

    def __str__(self):
        a = "lat: %s, long: %s, r: %s, theta: %s" % (self.lat, self.long, self.r, self.theta)
        return a


class TravelPolygon:
    def __init__(self, latitude, longitude, max_time, slices):
        self.slices = slices
        self.points = []
        self.max_time = max_time

        r_init = 1.0/69 # 1 mile ish
        for theta in range(0, 360, 360/slices):
            point = Point(r_init, theta, latitude, longitude)
            self.points.append(point)
  
    def __str__(self):
        s = ""
        for point in self.points:
            s += "%s, %s\n" % (point.long, point.lat)
        return s
    

    def fit(self):
        pass
        

    def __update(self):
        pass



shape = TravelPolygon(37.788889, -122.399864, 10, 50)
