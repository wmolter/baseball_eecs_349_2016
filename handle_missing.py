import sys
def main():
    in_file = open(sys.argv[1])
    output = open(sys.argv[2], 'w')
    for line in in_file:
        output.write(line.replace("None", "?"))



if __name__ == "__main__":
    main()