"""
Kelly Brennan and Celine Ta
Software Design Spring 2015
Interactive Visualization Project

We aim to create an interactive map that displays each countries' happiness rating and GDP
"""
import state_boundaries
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


		self.state_xs = [state_boundaries.data[code]['lons'] for code in state_boundaries.data]
		self.state_ys = [state_boundaries.data[code]['lats'] for code in state_boundaries.data]

		# Read data from CSV file
		df = pd.read_csv('data/GDP_per_state.csv', names = ['State', 'GDP'])
		self.state_GDP = dict(zip(df.State, df.GDP))

		stats = pd.read_csv('data/happiness_UScentric.csv')
		data_states = stats['What state or province do you live in, if applicable?']
		data_happy = stats['Do you love and appreciate yourself?']
		data_safety = stats['Are your surroundings physically safe?']

		# self.states = dict(zip(self.state_GDP.keys(), [State(self.state_GDP.keys()[i],0,0,0,0,0) for i in range(len(self.state_GDP.keys()))])) # create master dictionary of State objects
		self.states = dict(zip(state_boundaries.data.keys(), [State(state_boundaries.data.keys()[i],0,0, self.state_GDP[name], state_boundaries.data[name]['lons'], state_boundaries.data[name]['lats']) for i,name in enumerate(state_boundaries.data.keys())]))
		# fill in self.states with State objects with their own happiness and safety ratings
		for i in range(len(data_states)):
			tryState =	data_states[i]
			if tryState in self.states and tryState in state_boundaries.data:
				self.states[tryState].add_happiness_safety(data_happy[i], data_safety[i])			
		# print self.states
		# averages Happiness and Safety ratings for each State on master dictionary
		#for k in self.states.keys():
		for v in self.states.values():
			if len(v.happiness) >= 2: #checking we got at least one actual entry
				v.average_data()

		# print self.states.values()
		# for i in self.states.values():
		# 	print i
		# print getattr(self.states.values(), 'get_GDP')


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
		xs = []
		ys = []

		# print len(self.states.keys())
		for st in self.states.values():
			if type(st) is not str:
				names.append(st.name)
				happiness.append(st.happiness)
				safety.append(st.safety)
				grossDP.append(st.GDP)
				xs.append(st.borderX)
				ys.append(st.borderY)

		# TODO: IS THERE ANY WAY TO GET OBJECT INFO INTO PATCHES OR TOOLTIPS?
		# source = bk.ColumnDataSource(
	 #    	data=dict(
		#         name=names,
		#         happiness=happiness,
		#         safety=safety,
		#         GDP=grossDP,
		#         state_xs = state_xs,
		#         state_ys = state_ys
  #  			 )
		# )
		# print len(names)
		print names

		bk.output_file("Map_bk.html", title="Hello World!")  # save plot as html
		fig = bk.figure(plot_width = 600, plot_height= 600, title = "Map", tools = TOOLS) #creates new Bokeh plot

		fig.patches (xs, ys,
			fill_color = state_colors, fill_alpha = 0.7, 
			source = bk.ColumnDataSource(data = {
				    'state':names,
				    'happiness': happiness, 
				    'GDP': grossDP
				}),
			line_color = "black", line_width = 0.5)

		# fig.patches (state_xs, state_ys,
		# 	fill_color = state_colors, fill_alpha = 0.7, 
		# 	line_color = "black", line_width = 0.5)
		#pdb.set_trace()

		#fig.text(self.state_xs, self.state_ys, # can't recognize coordinates as value on chart
    	#	text=self.states.keys(),text_color="#333333",
    	#	text_align="center", text_font_size="10pt")

		hover = fig.select(dict(type = hov))
		# hover.snap_to_data = False
		hover.tooltips = OrderedDict([("State", "@state"), ("Happiness", "@happiness"), ("GDP", "@GDP")])#, ("GDP", "@GDP")])
				# hover.snap_to_data = False

		# hover.tooltips = ([('State:', '@state'), ("(x,y)", "($x, $y)")], [('Happiness', '@happiness')])

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

	def __str__(self):
		return self.name + str(self.happiness) + "," + str(self.safety) + "," + str(self.GDP) + str(self.borderX) + str(self.borderY)

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

