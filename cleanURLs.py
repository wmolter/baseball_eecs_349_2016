import requests

urls = open('urls.txt')
workingUrls = open('cleanURLs.txt', 'w')
count = 1

for url in urls:
	if count % 10 == 0:
		print 'Cleaning ' + str(count) + ' urls\n'
	url = url.strip()
	r = requests.get(url)
	if url == r.url:
		workingUrls.write(url+'\n')
		print 'Found one!'
	count += 1

workingUrls.close()