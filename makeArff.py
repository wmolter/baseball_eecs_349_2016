import os.path
import sys
import json

def main():
    input_file = sys.argv[1]
    out_filename = sys.argv[2]

    infile = open(input_file, 'r')
    output = open(out_filename, 'w')
    output.write("@relation training\n")

    entry = infile.readline()
    lineDict = json.loads(entry)
    for key in lineDict.keys():
        if key == 'away_team' or key == 'home_team':
            continue
        elif key[1] == 'b':# and int(key[2]) < 5:
            for key1 in lineDict[key].keys():
                if key1 == 'OBP' or key1 == 'BA':
                    output.write("@attribute " + key + '_' + key1 + ' numeric\n')
        elif key == 'winner':
            output.write("@attribute " + key + ' {True, False}\n')
        elif key[-1] =='p':
            output.write('@attribute ' + key + " numeric\n")
        #output.write("\n")

    startIndex = int(sys.argv[3])
    endIndex = -1
    try:
        endIndex = int(sys.argv[4])
    except Exception:
        pass

    output.write("\n@data\n")
    index = 0

    while entry != '' and (index <= endIndex or endIndex == -1):
        lineDict = json.loads(entry)
        if index % 5000 == 0:
            print 'Processing ' + str(index) + ' lines.'
        if index >= startIndex:
            line = ''
            for key in lineDict.keys():
                if key == 'away_team' or key == 'home_team':
                    continue
                elif key[1] == 'b':# and int(key[2]) < 5:
                    for key1 in lineDict[key].keys():
                        if key1 == 'OBP' or key1 == 'BA':
                            line += str(lineDict[key][key1])+','
                elif key[-1] == 'p':
                    line += str(lineDict[key])+','
            line = line[:-1]
            output.write(line +'\n')

        entry = infile.readline()
        index += 1
    output.close()

main()
