
from bs4 import BeautifulSoup
import requests
import os.path
import sys
import json

# Command line arguments: output file name, folder of files, start index of files, optional end index of files
def main():

    out_filename = sys.argv[1]

    output = open(out_filename, 'w')
    '''output.write("@relation training\n")
    metadata = get_attrib_metadata()
    for attrib in metadata:
        output.write("@attribute " + attrib["name"])
        if attrib["is_nominal"]:
            output.write(" {")
            output.write(",".join(str(x) for x in attrib["is_nominal"]))
            output.write("}")
        else:
            output.write(" numeric")
        output.write("\n")'''

    folder = sys.argv[2]
    startIndex = int(sys.argv[3])
    endIndex = -1
    try:
        endIndex = int(sys.argv[4])
    except Exception:
        pass

    #output.write("\n@data\n")
    index = startIndex
    pathname = folder + "/HTML File_" + str(index) + ".html"
    while index <= endIndex or endIndex == -1 and os.path.exists(pathname):
        if index % 100 == 0:
            print "Processing " + str(index) + " files."
        if os.path.exists(pathname):
            this_file = open(pathname)
            cont = this_file.read()
            parsed_box = parse_one_box(cont)
            dump = json.dumps(make_dump(parsed_box))
            #csv = ','.join(str(x) for x in cleaned_box)
            output.write(dump + "\n")
            this_file.close()
        index += 1
        pathname = folder + "/HTML File_" + str(index) + ".html"
    output.close()



#  Takes in a box score html file and returns a dictionary with the winner and 4 tables: home_batting, away_batting,
#  home_pitching, and away_pitching, which contain the full contents of the tables in the html file except for the
#  name.
def parse_one_box(html):
    soup = BeautifulSoup(html, "html.parser")

    content = soup.find(id='page_content')
    score = content.find_all(class_="xxx_large_text bold_text", limit=2)
    winner = int(score[0].string) > int(score[1].string)

    tables = content.find_all(class_="sortable stats_table", limit=4)

    all_data = [] #3D array of 4 tables
    for table in tables:
        this_table = []
        categories = table.find("thead").find("tr").find_all()
        category_names = (child.string for child in categories)
        for row in table.find("tbody").find_all("tr"):
            entries = row.find_all("td")
            data_strings = (entry.string for entry in entries[1:-1])
            data_numbers = []
            for entry in data_strings:
                if entry is None:
                    data_numbers.append("?")
                else:
                    data_numbers.append(float(entry))
            this_table.append(data_numbers)
        all_data.append(this_table)

    return {"winner":winner, "home_batting": all_data[0], "away_batting": all_data[1],
            "home_pitching": all_data[2], "away_pitching": all_data[3]}


#  This function takes in the output from parse_one_box and returns a list of attribute values for that box score:
#  ["home_avg", "home_obp", "home_slg", "home_ops", "home_era", "away_avg", "away_obp", "away_slg", "away_ops", "away_era","winner"]
#  in that order.  The batting stats are the average of each team's stats over the players; the pitching stats are just
#  for the starting pitcher.
'''def clean_box_for_tree(box_dict):
    winner = [box_dict["winner"]]
    h_bat = box_dict["home_batting"]
    a_bat = box_dict["away_batting"]

    home_avgs = average_columns(h_bat, 7, 11)
    away_avgs = average_columns(a_bat, 7, 11)
    h_era = [box_dict["home_pitching"][0][7]]
    a_era = [box_dict["away_pitching"][0][7]]
    this_row =home_avgs + h_era + away_avgs + a_era + winner
    return this_row'''

#function takes in the output from parse_one_box and returns a dictionary to be handed to json.dumps() in the 
#format {winner: , hb1-9: , ab1-9: , hp: , ap: }
def make_dump(box_dict):
    new_dict = {'winner': box_dict['winner']}
    for i in range(0, 9):
        new_dict[('hb'+str(i))] = {'BA':box_dict['home_batting'][i][7], 'OBP':box_dict['home_batting'][i][8], 'SLG':box_dict['home_batting'][i][9], 'OPS':box_dict['home_batting'][i][10]}
        new_dict[('ab'+str(i))] = {'BA':box_dict['away_batting'][i][7], 'OBP':box_dict['away_batting'][i][8], 'SLG':box_dict['away_batting'][i][9], 'OPS':box_dict['away_batting'][i][10]}
    new_dict['hp'] = box_dict['home_pitching'][0][7]
    new_dict['ap'] = box_dict['away_pitching'][0][7]
    return new_dict
#  This averages the columns of table from start_index to end_index into a list of end_index-start_index values (the
#  average of those columns).
'''def average_columns(table, start_index, end_index):
    avgs = []
    for index in range(start_index, end_index):
        values = [row[index] for row in table if row[index] is not None]
        avg = sum(values)/len(values)
        avgs.append(avg)
    return avgs'''


# This functions a list of attribute dictionaries, with "name" and "is_nominal" mapped to their respective values.
'''def get_attrib_metadata():
    attribs = ["home_avg", "home_obp", "home_slg", "home_ops", "home_era", "away_avg", "away_obp", "away_slg", "away_ops", "away_era","away_winner"]
    i = 0
    metadata = []
    for attrib in attribs:
        metadata.append({})
        metadata[i]["name"] = attrib
        metadata[i]["is_nominal"] = False
        i += 1
    metadata[i-1]["is_nominal"] = [True, False]
    return metadata'''



if __name__ == "__main__" :
    main()
