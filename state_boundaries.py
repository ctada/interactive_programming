
import csv
import xml.etree.cElementTree as et


US_states = open("data/US Regions State Boundaries.csv")
nan = float('NaN')


data = {}
with US_states as f:
    next(f)
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
    	region, state, state_id, geometry, color = row

        # # print type(geometry)
        # print state
        # print geometry
        # print type(et.fromstring(geometry))
    	xml = et.fromstring(geometry)
        lats = []
        lons = []
        for i, poly in enumerate(xml.findall('.//outerBoundaryIs/LinearRing/coordinates')):
            if i > 0:
                lats.append(nan)
                lons.append(nan)
            coords = (c.split(',')[:2] for c in poly.text.split())
            lat, lon = list(zip(*[(float(lat), float(lon)) for lon, lat in
                coords]))
            lats.extend(lat)
            lons.extend(lon)
        data[state] = {
            'region' : region,
            'state' : state,
            'lats' : lats,
            'lons' : lons,
        }#Code above is based off of Bokeh Texas example code: US_counties.py
#print type(data['Oregon']['lats'])
# return data
#print type(data['California'][1])
