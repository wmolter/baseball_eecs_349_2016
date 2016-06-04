import sys
import requests


#  This file gets the .html files from baseball-reference.com for every team for every year between
#  the start and end year specified (inclusive).

#  Command line arguments:  folder to store files in, start year, end year
#  ex. team_htmls.py teams 2001 2015
def main():
    print "ran this"
    folder = sys.argv[1]
    start_year = int(sys.argv[2])
    fin_year = int(sys.argv[3])

    url_file = open(folder + "/team_urls" + str(start_year) + "-" + str(fin_year) + ".txt", 'w')
    teams = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'ANA', 'LAD', 'FLA', 'MIL', 'MIN', 'MON', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'STL', 'TBD', 'TEX', 'TOR', 'WSN']
    url_head = "http://www.baseball-reference.com"
    for team in teams:
        print "ran for a team"
        for year in range(start_year, fin_year+1):
            url_tail = "/teams/" + team + "/" + str(year) + ".shtml"
            full_url = url_head + url_tail
            url_file.write(full_url + "\n")
            html_page = requests.get(full_url)
            curr_file = open(folder + "/" + team + str(year) + ".html", 'w')
            curr_file.write(html_page.content)
            curr_file.close()
    url_file.close()




if __name__ == "__main__":
    main()
