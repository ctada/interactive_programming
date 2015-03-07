"""
Boston map testing with Kartograph
"""

from kartograph import Kartograph
K = Kartograph()
# hopfulMap = open('Bos_neighborhoods_test.json')
K.generate(open('Bos_neighborhoods_text.json'), outfile = 'myBosMap.svg')