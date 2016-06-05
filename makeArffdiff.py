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
                continue
                #if key1 == 'SLG':# or key1 == 'OBP':
                output.write("@attribute " + key + '_' + key1 + ' numeric\n')
        elif key == 'winner':
            output.write("@attribute " + key + ' {True, False}\n')
        elif key[-1] =='p':
            #continue
            output.write('@attribute ' + key + " numeric\n")
        #output.write("\n")
    for i in range(0,9):
        output.write('@attribute b' + str(i) + 'BAdiff numeric\n')
        output.write('@attribute b' + str(i) + 'OBPdiff numeric\n')
        output.write('@attribute b' + str(i) + 'SLGdiff numeric\n')
        output.write('@attribute b' + str(i) + 'OPSdiff numeric\n')
    
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
                        continue
                        #if key1 == 'SLG':# or key1 == 'OBP':
                        line += str(lineDict[key][key1])+','
                elif key == 'winner' or key[-1] == 'p':
                    line += str(lineDict[key])+','
            for i in range(0, 9):
                if lineDict['hb'+str(i)]['BA'] == '?' or lineDict['ab'+str(i)]['BA'] == '?':
                    line += '?,'
                else:
                    line += str(float(lineDict[('hb'+str(i))]['BA'])-float(lineDict[('ab'+str(i))]['BA'])) +','
                if lineDict['hb'+str(i)]['OBP'] == '?' or lineDict['ab'+str(i)]['OBP'] == '?':
                    line += '?,'
                else:
                    line += str(float(lineDict[('hb'+str(i))]['OBP'])-float(lineDict[('ab'+str(i))]['OBP'])) +','
                if lineDict['hb'+str(i)]['SLG'] == '?' or lineDict['ab'+str(i)]['SLG'] == '?':
                    line += '?,'
                else:
                    line += str(float(lineDict[('hb'+str(i))]['SLG'])-float(lineDict[('ab'+str(i))]['SLG'])) +','
                if lineDict['hb'+str(i)]['BA'] == '?' or lineDict['ab'+str(i)]['BA'] == '?':
                    line += '?,'
                else:
                    line += str(float(lineDict[('hb'+str(i))]['OPS'])-float(lineDict[('ab'+str(i))]['OPS'])) +','
            line = line[:-1]
            output.write(line +'\n')

        entry = infile.readline()
        index += 1
    output.close()

main()
