import sys, getopt

# print('Number of arguments:' + str(len(sys.argv)) + 'arguments.')
# print('Argument List:' + str(sys.argv))

def main(argv):
    wordsize = ''
    inputfile = ''
    outputfile = ''
    mainUsage = 'test.py -w <size> -i <inputfile> -o <outputfile>'
    try:
        opts, args = getopt.getopt(argv,"hw:i:o:",["wsize=","ifile=","ofile="])
    except getopt.GetoptError:
        print(mainUsage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(mainUsage)
            sys.exit()
        elif opt in ("-w", "--wsize"):
            wordsize = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        
    print('Word size is ' + wordsize)
    print('Input file is ' + inputfile)
    print('Output file is ' + outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])