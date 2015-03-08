"""
Kelly Brennan and Celine Ta
Software Design Spring 2015
Interactive Visualization Project

We aim to create an interactive map that displays each countries' happiness rating and GDP
"""
import bokeh.plotting as bk
import numpy as np
from bokeh.models import HoverTool as hov
import pandas as pd
from bokeh.charts import Scatter
from collections import OrderedDict

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
		#for now, data is not related to geography
		#stats = pd.read_csv('data/happiness_UScentric.csv')
		#self.states = stats['What state or province do you live in, if applicable?']
		#self.year = stats['Do you love and appreciate yourself?']
		#self.safety = stats['Are your surroundings physically safe?']
		#df = stats[["Do you love and appreciate yourself?", "Are your surroundings physically safe?", "What state or province do you live in, if applicable?"]]
		#g = df.groupby('What state or province do you live in, if applicable?')
		#self.pdict = OrderedDict()

		#for i in g.groups.keys():
		#    labels = g.get_group(i).columns
		#    xname = labels[0]
		#    yname = labels[1]
		#    x = getattr(g.get_group(i), xname)
		#    y = getattr(g.get_group(i), yname)
		#    pdict[i] = zip(x, y)

		# any of the following commented are valid Scatter inputs
		#xyvalues = pdict
		#xyvalues = pd.DataFrame(xyvalues)
		#xyvalues = xyvalues.values()
		#xyvalues = np.array(xyvalues.values())

		#self.juvRate=[]
		#for rate in stats['Rate per 100,000']:
		#	if not np.isnan(rate):
		#		self.juvRate.extend(int(rate))
		
		#TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,previewsave"
		#scatter = Scatter(
		#    self.pdict, filename="state_happiness.html", tools=TOOLS, ylabel='Physical Safety'
		#)
		#scatter = Scatter(g, filename="state_happiness.html", title="State Happiness GroupBy")
		#scatter.show()


		df = pd.read_csv('data/GDP_per_state.csv', names = ['State', 'GDP'])
		self.state_GDP = dict(zip(df.State, df.GDP))


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
		bk.output_file("Map_bk.html", title="Hello World!")  # save plot as html
		fig = bk.figure(plot_width = 600, plot_height= 600, title = "Map") #creates new Bokeh plot
		#fig.circle(#self.gender, self.year,
         #size=(self.juvRate), # px
         #xs, ys,
         #size =2,
         #fill_alpha=0.5,
         #fill_color="steelblue",
         #line_alpha=0.8,
         #line_color="crimson")
		#fig.circle(xs,ys)

		#fig.line(xs, ys, line_width=2)

		#TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,previewsave"
		#scatter = Scatter(
		#    self.state_GDP, filename="state_happiness.html", tools=TOOLS, ylabel='State GDP'
		#)
		#scatter.show()

		bk.save(obj=fig)
		bk.show(fig)

class Country():
	def __init__(self,name, borders, happiness, GDP):
		"""
		Creates Country object with name, borders, mean happiness level, and GDP of a certain year
		"""
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
		pass
	def get_mouse_position(self):
		"""
		returns mouse position in relation to map image (translate from screen position)
		"""
		pass
if __name__ == '__main__':
	vis = Display_Map() # pass in arguments
	#mouse = Interactive() 
	vis.run_display()