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
            pass
        elif key[1] == 'b':
            for key1 in lineDict[key].keys():
                output.write("@attribute " + key + '_' + key1 + ' numeric\n')
        elif key == 'winner':
            output.write("@attribute " + key + ' {True, False}\n')
        else:
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
        if index % 100 == 0:
            print 'Processing ' + str(index) + ' lines.'
        if index >= startIndex:
            line = ''
            for key in lineDict.keys():
                if key == 'away_team' or key == 'home_team':
                    pass
                elif key[1] == 'b':
                    for key1 in lineDict[key].keys():
                        line += str(lineDict[key][key1])+','
                else:
                    line += str(lineDict[key])+','
            line = line[:-1]
            output.write(line +'\n')

        entry = infile.readline()
        index += 1
    output.close()

main()
