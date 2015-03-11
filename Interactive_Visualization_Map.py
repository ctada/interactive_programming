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
from bokeh.models import HoverTool as hov
import pandas as pd
from collections import OrderedDict
import pdb

class Display_Map(object):
	"""
	Takes in map image, array of defining coordinates for each State, and list of countries. Upon a mouse action, Display_Map will
	look up location of mouse action in relation to map and update display accordingly.
	"""
	#def __init__(self,image, borders, list_countries):
	def __init__(self):
		"""
		Initializes map image, borders, countries
		"""

		# US Geography data processing for map generation
		US_states = open("data/US Regions State Boundaries_processed.csv")
		nan = float('NaN')

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
		self.state_xs = [boundary_data[code]['lons'] for code in boundary_data]
		self.state_ys = [boundary_data[code]['lats'] for code in boundary_data]

		# Read data from CSV file
		df = pd.read_csv('data/GDP_per_state.csv', names = ['State', 'GDP'])
		self.state_GDP = dict(zip(df.State, df.GDP))

		stats = pd.read_csv('data/happiness_UScentric.csv')
		data_states = stats['What state or province do you live in, if applicable?']
		data_happy = stats['Do you love and appreciate yourself?']
		data_safety = stats['Are your surroundings physically safe?']

		self.states = {} # create master dictionary of State objects
		
		# fill in self.states with State objects with their own happiness and safety ratings
		for i in range(len(data_states)):
			tryState =	data_states[i]
			if tryState in self.state_GDP and tryState in boundary_data.keys(): #ensures territory is in US and we have info for it
				if tryState in self.states: #then they should also be in self.state_safe
					self.states[tryState].add_happiness_safety(data_happy[i], data_safety[i])				
				else:
					boundariesX = boundary_data[tryState]['lons']
					boundariesY = boundary_data[tryState]['lats']
					self.states[tryState] = State(tryState, data_happy[i], data_safety[i], self.state_GDP[tryState], boundariesX, boundariesY)

		# averages Happiness and Safety ratings for each State on master dictionary
		for k in self.states.keys():
			self.states[k].average_data()


	def run_display(self):
		"""
		Maintains display/ interaction experience
		"""
		colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
		state_colors = ["#F1EEF6"] #NEEDS TO BE SET IN LATER CODE

		TOOLS = "pan, wheel_zoom, box_zoom, reset, hover"

		# Pull info from each State in self.states for use in bokeh
		names = []
		happiness = []
		safety = []
		grossDP = []
		state_xs = []
		state_ys = []

		for elem in self.states.keys():
			state_obj = self.states[elem]
			names.append(state_obj.get_name())
			happiness.append(state_obj.get_happiness())
			safety.append(state_obj.get_safety())
			grossDP.append(state_obj.get_GDP)
			state_xs.append(state_obj.getX())
			state_ys.append(state_obj.getY())

		# TODO: IS THERE ANY WAY TO GET OBJECT INFO INTO PATCHES OR TOOLTIPS?
		source = bk.ColumnDataSource(
	    	data=dict(
		        name=names,
		        happiness=happiness,
		        safety=safety,
		        GDP=grossDP,
		        state_xs = state_xs,
		        state_ys = state_ys
   			 )
		)

		bk.output_file("Map_bk.html", title="Hello World!")  # save plot as html
		fig = bk.figure(plot_width = 600, plot_height= 600, title = "Map", tools = TOOLS) #creates new Bokeh plot

		fig.patches (state_xs, state_ys,
			fill_color = state_colors, fill_alpha = 0.7, 
			line_color = "black", line_width = 0.5)
		#pdb.set_trace()

		#fig.text(self.state_xs, self.state_ys, # can't recognize coordinates as value on chart
    	#	text=self.states.keys(),text_color="#333333",
    	#	text_align="center", text_font_size="10pt")

		hover = fig.select(dict(type = hov))
		# hover.snap_to_data = False
		hover.tooltips = OrderedDict([("State", "@names"), ("GDP", "@GDP")])

		bk.save(obj=fig)
		bk.show(fig)

class State():
	def __init__(self,name,happiness, safety, GDP, borderX, borderY):
		"""
		Creates State object with name, mean happiness level, and contribution to GDP of a certain year
		"""
		self.name = name
		self.happiness = [happiness]
		self.safety = [safety]
		self.GDP = GDP
		self.borderX = borderX
		self.borderY = borderY

	def get_name(self):
		"""returns name"""
		return self.name

	def get_happiness(self):
		"""
		returns State's mean happiness level
		"""
		return self.happiness

	def get_GDP(self):
		"""
		returns State's contribution to GDP
		"""
		return self.GDP

	def get_safety(self):
		"""
		returns safety level
		"""
		return self.safety

	def getX(self):
		"""
		returns x-position perimeter coordinates
		"""
		return self.borderX

	def getY(self):
		"""
		returns y-position perimeter coordinates
		"""
		return self.borderY

	def add_happiness_safety(self, hapVal, safeVal):
		"""
		No return. Records happiness and safety rating to State object.
		"""
		self.happiness.append(hapVal)
		self.safety.append(safeVal)

	def average_data(self):
		""" 
		No return. Averages a state's happiness, safety
		"""
		self.happiness = float(sum(self.happiness))/len(self.happiness)
		self.safety = float(sum(self.safety))/len(self.safety)


class Interactive():
	def __init__(self):
		"""
		Initializes monitoring of user input
		"""
		hover = fig.select(dict(type = HoverTool))
		# hover.snap_to_data = False
		hover.tooltips = [("(x,y)", "($x, $y)")]

		show(fig)

	def get_mouse_position(self):
		"""
		returns mouse position in relation to map image (translate from screen position)
		"""
		pass
if __name__ == '__main__':
	vis = Display_Map() # pass in arguments
	#mouse = Interactive() 
	vis.run_display()

