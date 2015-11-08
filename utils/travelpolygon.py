import os
import math as math
import googlemaps
import datetime as datetime


token = os.getenv("GOOGLE_TOKEN", "notatoken")
#print(token)
gmaps = googlemaps.Client(key=token)

class Point:
    def __init__(self, r, theta, start_long, start_lat):
        self.r = r
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
    def __init__(self, latitude, longitude, max_time, slices):
        self.slices = slices
        self.points = []
        self.max_time = max_time
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

    def fit(self):
        for point in self.points:
            if not point.done:
                pointLatLong = str(point.lat) + ','+ str(point.long)
                startLatLong = str(self.centerLat)+ ',' + str(self.centerLong)
                a = datetime.datetime(2015,11,9,8,0,0) 
                travelTime =(gmaps.distance_matrix(startLatLong,pointLatLong,mode='driving',departure_time=a))
                travelTime = travelTime['rows'][0]['elements'][0]['duration']['value']
                thresholdTime = (abs(self.max_time - travelTime))/self.max_time 
                print(str(point) + " -- " + str(travelTime))
                # if(thresholdTime < 1.1 and thresholdTime > .9):
                #     point.done = True
                # elif (travelTime > self.max_time):
                #     adjustR(point,'decrease')
                # elif(travelTime < self.max_time):
                #     adjustR(point,'increase')
     #def adjustR(point,adjustVal):
        #if(adjustVal = 'decrease'):

    def __update(self):
        pass



#shape = TravelPolygon(37.788889, -122.399864, 2, 4)
#shape.fit()
#print(shape)
