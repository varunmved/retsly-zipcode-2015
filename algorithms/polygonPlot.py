'''
 x = r*cos(theta)
 y = r*sin(theta)

'''
import math as math

NUM_OF_SLICES = 50

pointsList = []

class point:

    def __init__(self, r, theta, start_long, start_lat):
        self.r = r
        self.theta = math.radians(theta)
        self.long = start_long + (r * math.cos(self.theta))
        self.lat = start_lat + (r * math.sin(self.theta))
        self.done = False

    def __str__(self):
        #a = "lat: %s, long: %s, r: %s, theta: %s" % (self.lat, self.long, self.r, self.theta)
        a = str(self.lat)  + ',' + str(self.long)
        return a


def buildPoint(startLat,startLongi,degree, rIn):
    #init
    thisPoint = point(rIn, degree, startLongi, startLat)
    #pass to appender
    print(thisPoint)
    pointsList.append(thisPoint)


def start(startLat,startLongi):
    rIn = 1.0/69
    #for(i = 0, i < 360; i+=360.00/NUM_OF_SLICES):
    for i in range(0,360,360/NUM_OF_SLICES):
        buildPoint(startLat,startLongi,i,rIn)
        #i+=360.00/NUM_OF_SLICES

start(37.788889, -122.399864)

