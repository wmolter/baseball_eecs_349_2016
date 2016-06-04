import json
import sys

def main():
    in_file = open(sys.argv[1])

    raw_json = in_file.read()  # yes, this loads several megabytes into memory, but it's okay.
    in_file.close()
    full_data = json.loads(raw_json)

    out_data = {}  # might be large also, again, it's not THAT large.
    index = 0
    attribs = []  # list of dictionaries for attributes

    for team_year in full_data:
        all_tables = full_data[team_year]
        this_team = {}

        bat_value_totals = all_tables["players_value_batting"]["totals"]["Team Total"]
        bat_value_headings = all_tables["players_value_batting"]["headings"]
        start_index = bat_value_headings.index("Rbat")
        end_index = bat_value_headings.index("Salary")
        for i in range(start_index, end_index+1):
            heading = bat_value_headings[i]
            attrib_name = "bat_" + heading
            if index == 0:
                attribs.append({"name": attrib_name, "type": "numeric"})
            this_team[attrib_name] = bat_value_totals[i]

        pitch_value_totals = all_tables["players_value_pitching"]["totals"]["Team Total"]
        pitch_value_headings = all_tables["players_value_pitching"]["headings"]
        start_index = pitch_value_headings.index("RA9")
        end_index = pitch_value_headings.index("Salary")
        for i in range(start_index, end_index+1):
            heading = pitch_value_headings[i]
            attrib_name = "pitch_" + heading
            if index == 0:
                attribs.append({"name": attrib_name, "type": "numeric"})
            this_team[attrib_name] = pitch_value_totals[i]

        field_totals = all_tables["standard_fielding"]["totals"]["Team Totals"]
        field_headings = all_tables["standard_fielding"]["headings"]
        start_index = field_headings.index("Fld%")
        end_index = field_headings.index("RF/G")
        for i in range(start_index, end_index+1):
            heading = field_headings[i]
            attrib_name = "field_" + heading
            if index == 0:
                attribs.append({"name": attrib_name, "type": "numeric"})
            this_team[attrib_name] = field_totals[i]



        out_data[team_year] = this_team
        index += 1

    out_data["attribs"] = attribs
    out_file = open(sys.argv[2], 'w')
    out_file.write(json.dumps(out_data, indent=4))
    out_file.close()


if __name__ == "__main__":
    main()