
from bs4 import BeautifulSoup
import requests

def main():

    url = "http://www.baseball-reference.com/boxes/OAK/OAK200408250.shtml"
    r = requests.get(url)
    cont = r.content
    parsed_box = parse_one_box(cont)
    cleaned_box = clean_box_for_tree(parsed_box)
    print(cleaned_box)




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
                    data_numbers.append(None)
                else:
                    data_numbers.append(float(entry))
            this_table.append(data_numbers)
        all_data.append(this_table)

    # print "The winner is " + str(winner)
    # for row in all_data:
    #     print list(row)
    return {"winner":winner, "home_batting": all_data[0], "away_batting": all_data[1],
            "home_pitching": all_data[2], "away_pitching": all_data[3]}


def clean_box_for_tree(box_dict):
    winner = [box_dict["winner"]]
    h_bat = box_dict["home_batting"]
    a_bat = box_dict["away_batting"]

    home_avgs = average_columns(h_bat, 7, 11)
    away_avgs = average_columns(a_bat, 7, 11)
    h_era = [box_dict["home_pitching"][0][7]]
    a_era = [box_dict["away_pitching"][0][7]]
    this_row = winner + home_avgs + h_era + away_avgs + a_era
    return this_row

def average_columns(table, start_index, end_index):
    avgs = []
    for index in range(start_index, end_index):
        values = [row[index] for row in table if row[index] is not None]
        avg = sum(values)/len(values)
        avgs.append(avg)
    return avgs

def get_attrib_metadata():
    attribs = ["winner", "home_avg", "home_obp", "home_slg", "home_ops", "home_era", "away_avg", "away_obp", "away_slg", "away_ops", "away_era"]
    i = 0
    metadata = []
    for attrib in attribs:
        metadata.append({})
        metadata[i]["name"] = attrib
        metadata[i]["is_nominal"] = False
        i += 1
    metadata[0]["is_nominal"] = True
    return metadata



if __name__ == "__main__" :
    main()
