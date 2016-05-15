#http://www.baseball-reference.com/boxes/ARI/ARI201403220.shtml
#28: 2, 30: 4, 6, 9, 11  


def generateURL():
	baseString = 'http://www.baseball-reference.com/boxes/'
	stringEnd = '0.shtml\n'
	teams = ['ARI', 'ATL', 'BAL', 'BOS', 'CHN', 'CHA', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCA', 'ANA', 'LAN', 'MIA', 'MIL', 'MIN', 'NYN', 'NYA', 'OAK', 'PHI', 'PIT', 'SDN', 'SEA', 'SFN', 'SLN', 'TBA', 'TEX', 'TOR', 'WAS']
	years = []
	recentYear = 2015
	oldestYear = 1980
	for year in range(recentYear, oldestYear-1, -1):
		years.append(str(year))
	months = []

	for month in range(3, 10):
			months.append('0'+str(month))
	days = []
	for day in range(1, 32):
		if day < 10:
			days.append('0'+str(day))
		else: 
			days.append(str(day))

	urls = open('urls.txt','w')

	for team in teams:
		for year in years:
			for month in months:
				if month == '04' or month == '06' or month == '09':
					for i in range(1, 30):
						urls.write(baseString+team+'/'+team+year+month+days[i]+stringEnd)
				elif month == '03': 
					for i in range(25, 31):
						urls.write(baseString+team+'/'+team+year+month+days[i]+stringEnd)
				else:
					for day in days:
						urls.write(baseString+team+'/'+team+year+month+day+stringEnd)

					
	urls.close()
generateURL()