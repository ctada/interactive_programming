import urllib2
from urllib2 import urlencode

# url = "http://example.com"
# website = urllib2.urlopen(url)
# print website.read()

# url = "http://example.com" #"http://google.com" 
# website = urllib2.urlopen(url)
# if url == website.geturl():
# 	print "Website not directed."
# else:
# 	print "Website redirected you."

# <?php
# echo $_POST['test'];
# ?>

url = "http://localhost/test.php"
data = {'test' : 'lolwut'}

encoded_data = urlencode(data)

website = urllib2.urlopen(url, encoded_data)
print website.read()