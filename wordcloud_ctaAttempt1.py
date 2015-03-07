"""Minimal attempt to check wordcloud"""
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS
import twitter
def get_tweets():
	location=[]
	api = twitter.Api(consumer_key='Kfrb1VZUZ4VnTeVSDDN35QHY0',
	                      consumer_secret='SL7uoE2TdOy8RH3RluHUiv44qNrU7kFUs6S47nQp37PommH5Bx',
	                      access_token_key='3070546828-38kCFOC3uXefqpRECYydBcXPDAzIlYEfsKceStu',
	                      access_token_secret='42KcNoPB6lrAQURlRo37OAmGAG4uUr8WwhWrZzKPLXERz')
	statuses = api.GetUserTimeline(screen_name='CoralMDavenport')
	for stat in statuses:
		location.append(stat.GetUser().GetLocation())
	print location

def make_cloud():
	d = path.dirname(__file__)

	# Read the whole text.
	text = open(path.join(d, 'alice.txt')).read()

	# read the mask image
	# taken from
	# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
	alice_mask = imread(path.join(d, "world1.png"))

	wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
	               stopwords=STOPWORDS.add("said"))
	# generate word cloud
	wc.generate(text)

	# store to file
	wc.to_file(path.join(d, "word_AliceWorld.png"))

	# show
	plt.imshow(wc)
	plt.axis("off")
	plt.figure()
	plt.imshow(alice_mask, cmap=plt.cm.gray)
	plt.axis("off")
	plt.show()

if __name__ == "__main__":
	get_tweets()
	make_cloud()