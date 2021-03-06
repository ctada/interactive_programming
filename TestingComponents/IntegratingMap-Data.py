"""
Kelly Brennan and Celine Ta
Software Design Spring 2015
Interactive Visualization Project

We aim to create an interactive map that displays each countries' happiness rating and GDP
"""
import csv
import xml.etree.cElementTree as et
import bokeh.plotting as bk
import numpy as np
from bokeh.models import HoverTool
import pandas as pd
import pdb

class Display_Map():
	"""
	Takes in map image, array of defining coordinates for each country, and list of countries. Upon a mouse action, Display_Map will
	look up location of mouse action in relation to map and update display accordingly.
	"""
	#def __init__(self,image, borders, list_countries):
	def __init__(self):
		"""
		Initializes map image, borders, countries
		"""
		# US Geography data processing for map generation
		US_states = open("US Regions State Boundaries.csv")
		nan = float('NaN')

		print type (self.state_boundaries)

		print self.state_boundaries

		# boundary_data = self.state_boundaries
		# print boundary_data[1]

		# self.state_xs = [boundary_data[code]['lons'] for code in boundary_data]
		# self.state_ys = [boundary_data[code]['lats'] for code in boundary_data]

		# Read data from CSV file
		df = pd.read_csv('GDP_per_state.csv', names = ['State', 'GDP'])
		self.state_GDP = dict(zip(df.State, df.GDP))

		stats = pd.read_csv('happiness_UScentric.csv')
		self.states = stats['What state or province do you live in, if applicable?']
		self.happy = stats['Do you love and appreciate yourself?']
		self.safety = stats['Are your surroundings physically safe?']

		self.state_hap = {}
		self.state_safe = {}
		# average happiness per state
		for i in range(len(self.states)):
			tryState = self.states[i]
			if tryState in self.state_hap: #then they should also be in self.state_safe
				self.state_hap[tryState].append(self.happy[i])
				self.state_safe[tryState].append(self.safety[i])
			#elif type(tryState) is 'str': # filter out nan types
			else:
				self.state_hap[tryState]=[self.happy[i]]
				self.state_safe[tryState]=[self.safety[i]]

		self.avgHap= [(i,float(sum(v))/len(v)) for i,v in self.state_hap.items()]
		self.avgSafe= [(i,float(sum(v))/len(v)) for i,v in self.state_safe.items()]


	def state_boundaries(self):
		"""
		Processes data for map of all the states
		"""
		boundary_data = {}
		with US_states as f:
		    next(f)
		    reader = csv.reader(f, delimiter=',', quotechar='"')
		    for row in reader:
		    	region, state, state_id, geometry, color = row
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
		        boundary_data[state] = {
		            'region' : region,
		            'state' : state,
		            'lats' : lats,
		            'lons' : lons,
		        }#Code above is based off of Bokeh Texas example code: US_counties.py
		return boundary_data

	def lookup_country(self,hover_pos):
		"""Given position, finds Country object
			returns: country (Country object)
		"""
		pass
	def update(self,hover_pos):
		"""
		Updates map display upon mouse action
		"""
		pass
	def run_display(self):
		"""
		Maintains display/ interaction experience
		"""
		colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
		state_colors = ["#DD1C77"] #NEEDS TO BE SET IN LATER CODE

		TOOLS = "pan, wheel_zoom, box_zoom, reset, hover"

		# bk.output_file("Map_bk.html", title="Hello World!")  # save plot as html
		# fig = bk.figure(plot_width = 600, plot_height= 600, title = "Map", tools = TOOLS) #creates new Bokeh plot
		# fig.patches (self.state_xs, self.state_ys,
		# 	fill_color = state_colors, fill_alpha = 0.7, 
		# 	line_color = "black", line_width = 0.5)
		# # fig.circle(x=zip(*self.avgHap)[1], y=zip(*self.avgSafe)[1], size= np.random.random(size=len(zip(*self.avgHap)[0])) * 15)# zip also splits dictionary into list of keys and list of values
		# #fig.circle(
  #        #xs, ys,
  #        #size =2,
  #        #fill_alpha=0.5,
  #        #fill_color="steelblue",
  #        #line_alpha=0.8,
  #        #line_color="crimson")
		
		# hover = fig.select(dict(type = HoverTool))
		# # hover.snap_to_data = False
		# hover.tooltips = ([("(x,y)", "($x, $y)")])
		# 	#("index:", boundary_data[index]),
		# # show(fig)

		# bk.save(obj=fig)
		# bk.show(fig)

class state():
	def __init__(self,name, borders, happiness, GDP):
		"""
		Creates Country object with name, borders, mean happiness level, and GDP of a certain year
		"""
		pass
	def get_state(self, lat, long):
		pass

	def get_happiness(self):
		"""
		returns country's mean happiness level
		"""
		pass
	def get_GDP(self):
		"""
		returns country's GDP
		"""
		pass

class Interactive():
	def __init__(self):
		"""
		Initializes monitoring of user input
		"""
		# hover = fig.select(dict(type = HoverTool))
		# # hover.snap_to_data = False
		# hover.tooltips = [("(x,y)", "($x, $y)")]

		# show(fig)

	def get_mouse_position(self):
		"""
		returns mouse position in relation to map image (translate from screen position)
		"""
		pass
if __name__ == '__main__':
	vis = Display_Map() # pass in arguments
	#mouse = Interactive() 
	vis.run_display()