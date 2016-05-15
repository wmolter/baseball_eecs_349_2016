import requests
import sys

urls = open(sys.argv[1])
workingUrls = open('clean' + sys.argv[1], 'w')
count = 1
index = 0

for url in urls:
	if count % 10 == 0:
		print 'Cleaning ' + str(count) + ' urls'
	url = url.strip()
	r = requests.get(url)
	if url == r.url:
		tempFileName = 'HTML File_' + str(index) + '.html'
		workingUrls.write(url+'\n')
		htmlFile = open(tempFileName, 'w')
		htmlFile.write(r.content)
		htmlFile.close()
		index += 1
		#print 'Found one!'
	count += 1

workingUrls.close()