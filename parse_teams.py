import sys
from bs4 import BeautifulSoup


def main():
    out_filename = sys.argv[1]
    start_year = int(sys.argv[2])
    fin_year = int(sys.argv[3])
    teams = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'ANA', 'LAD', 'FLA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'STL', 'TBD', 'TEX', 'TOR', 'WSN']

    for team in teams:
        for year in range(start_year, fin_year+1):
            curr_html_file = open(team + str(year) + ".html")
            curr_html_cont = curr_html_file.read()
            data = parse_one_team(curr_html_cont)

            url_tail = "/teams/" + team + "/" + str(year) + ".shtml"


def parse_one_team(html):
    soup = BeautifulSoup(html, "html.parser")
    soup.find(id='page_content')


if __name__ == "__main__":
    main()