"""
Kelly Brennan and Celine Ta
Software Design Spring 2015
Interactive Visualization Project

We aim to create an interactive map that displays each countries' happiness rating and GDP
"""
import state_boundaries # geographical data
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

	def __init__(self):
		"""
		Initializes map image, borders, countries
		"""
		
		# Read happiness and safety data from CSV file
		df = pd.read_csv('data/GDP_per_state.csv', names = ['State', 'GDP'])
		self.state_GDP = dict(zip(df.State, df.GDP))

		stats = pd.read_csv('data/happiness_UScentric.csv')
		data_states = stats['What state or province do you live in, if applicable?']
		data_happy = stats['Do you love and appreciate yourself?']
		data_safety = stats['Are your surroundings physically safe?']

		# Create dictionary of states that we want to display on map, with state name (string) as a key and State object as the value
		self.states = dict(zip(state_boundaries.data.keys(), [State(state_boundaries.data.keys()[i],0,0, self.state_GDP[name], state_boundaries.data[name]['lons'], state_boundaries.data[name]['lats']) for i,name in enumerate(state_boundaries.data.keys())]))
		
		# Add happiness and safety ratings to their corresponding States
		for i in range(len(data_states)):
			tryState =	data_states[i]
			if tryState in self.states and tryState in state_boundaries.data:
				self.states[tryState].add_happiness_safety(data_happy[i], data_safety[i])			

		# averages Happiness and Safety ratings for each State on master dictionary
		for v in self.states.values():
			if len(v.happiness) >= 2: #checking we got at least one actual entry besides the initial 0
				v.average_data()

	def run_display(self):
		"""
		Maintains display/ interaction experience
		"""
		colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
		state_colors = ["#4C0B5F"] # color of state is exists
		TOOLS = "pan, wheel_zoom, box_zoom, reset, hover"

		# Pull info from each State into attribute-specific lists for use in bokeh
		names = []
		happiness = []
		safety = []
		grossDP = []
		xs = []
		ys = []

		for st in self.states.values():
			if type(st) is not str:
				names.append(st.name)
				happiness.append(st.happiness)
				safety.append(st.safety)
				grossDP.append(st.GDP)
				xs.append(st.borderX)
				ys.append(st.borderY)

		bk.output_file("Map_bk.html", title="Hello World!")  # save plot as html
		fig = bk.figure(plot_width = 600, plot_height= 600, title = "Map", tools = TOOLS) #creates new Bokeh plot

		#display patches to match state shape, assigning state name, happiness, and GDP to each their respective patch
		fig.patches (xs, ys,
			fill_color = state_colors, fill_alpha = 0.7, 
			source = bk.ColumnDataSource(data = {
				    'state':names,
				    'happiness': happiness, 
				    'GDP': grossDP
				}),
			line_color = "black", line_width = 0.5)

		hover = fig.select(dict(type = hov)) # turn on hovering
		# hover.snap_to_data = False
		hover.tooltips = OrderedDict([("State", "@state"), ("Happiness", "@happiness"), ("GDP", "@GDP")]) # Customize what is displayed in tooltips
		
		bk.save(obj=fig) 
		bk.show(fig)

class State():
	def __init__(self,name,happiness, safety, GDP, borderX, borderY):
		"""
		Creates State object with name, mean happiness level, and contribution to GDP of a certain year
		"""
		self.name = name
		self.happiness = [happiness] #create list with happiness as the first entry
		self.safety = [safety] #create list with safety as the first entry
		self.GDP = GDP
		self.borderX = borderX
		self.borderY = borderY

	def __str__(self):
		return self.name + str(self.happiness) + "," + str(self.safety) + "," + str(self.GDP) + "," + str(self.borderX) + "," + str(self.borderY)

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
		self.happiness = float(sum(self.happiness))/(len(self.happiness)-1) # subtract one from denominator to get remove influence of initial State object set to 0 (added 0 happiness, safety to State's record)
		self.safety = float(sum(self.safety))/(len(self.safety)-1)

if __name__ == '__main__':
	vis = Display_Map() 
	vis.run_display()

