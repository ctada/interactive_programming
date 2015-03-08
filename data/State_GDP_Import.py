"""
Importing and processing stae GDP Data
"""

import pandas as pd

df = pd.read_csv('GDP_per_state.csv', names = ['State', 'GDP'])
print type(df)
# print df
print df.State
print df.GDP

state_GDP = dict(zip(df.State, df.GDP))
print state_GDP

# self.year = stats['Year'].Series.toList