import sys
from bs4 import BeautifulSoup
import json

# This file parses team html files into a json file containing data for each team for each year.
# Command line arguments: folder to find the html files, name of output file, starting year, and ending year.
# This relies on having used team_htmls.py to generate the files-- the naming convention it uses to find the html
# files is the same.
def main():
    folder = sys.argv[1]
    out_filename = sys.argv[2]
    start_year = int(sys.argv[3])
    fin_year = int(sys.argv[4])
    teams = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'ANA', 'LAA', 'LAD', 'FLA', 'MIA', 'MIL', 'MIN', 'MON', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'STL', 'TBD', 'TBR', 'TEX', 'TOR', 'WSN']

    output = open(out_filename, 'w')
    output.write("{\n\t")
    for team in teams:
        for year in range(start_year, fin_year+1):
            try:
                curr_html_file = open(folder + "/" + team + str(year) + ".html")
                curr_html_cont = curr_html_file.read()
                curr_html_file.close()
                data = parse_one_team(curr_html_cont)

            except StandardError:
                print "could not find data for " + team + " " + str(year)
                continue

            url_tail = "/teams/" + team + "/" + str(year) + ".shtml"
            output.write('"' + url_tail + '":')
            output.write(json.dumps(data))
            output.write(",\n")
    output.write("\n}")
    output.close()


def parse_one_team(html):
    soup = BeautifulSoup(html, "html.parser")
    soup.find(id='page_content')
    tables = soup.find_all(class_="sortable stats_table")
    if len(tables) == 0:
        raise StandardError("Could not find any stats tables for this html")

    output = {}
    for table in tables:
        table_key = table['id']
        heading_row = table.find("thead").find("tr")
        heading_tags = heading_row.find_all("th")
        headings = []
        for th in heading_tags:
            headings.append("".join(th.stripped_strings))
        output[table_key] = {}
        output[table_key]["headings"] = headings

        name_index = headings.index("Name")
        feet = table.find("tfoot").find_all("tr", class_="stat_total")
        totals = {}
        for row in feet:
            data_html = row.find_all('td')
            name = data_html[name_index].string
            #data_html = data_html[:name_index] + data_html[name_index+1:] #slices the name field out of this row
            info_in_row = []
            for cell in data_html:
                curr_string = cell.string
                if curr_string is None or curr_string == "":
                    curr_string = "?"
                elif curr_string[0] == '$':
                    curr_string = curr_string[1:]
                elif curr_string[-1] == '%':
                    curr_string = curr_string[:-1]
                info_in_row.append(curr_string)
            totals[name] = info_in_row
        output[table_key]["totals"] = totals

        body_rows = table.find("tbody").find_all("tr")
        body_data = []
        for row in body_rows:
            if row["class"] == "thead":
                continue
            cells = row.find_all("td")
            info_in_row = []
            for cell in cells:
                curr_string = "".join(cell.stripped_strings)
                curr_string = curr_string.replace(u"\xa0", " ")
                if curr_string is None or curr_string == "":
                    curr_string = "?"
                elif curr_string[0] == '$':
                    curr_string = curr_string[1:]
                elif not (curr_string[-1].isalpha() or curr_string[-1].isnumeric()):
                    curr_string = curr_string[:-1]
                info_in_row.append(curr_string)
            body_data.append(info_in_row)
        output[table_key]["individuals"] = body_data
    return output


if __name__ == "__main__":
    main()