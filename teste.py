import os, sys, getopt
# import operator, time, matplotlib.pyplot as plt # quando precisar, se precisar



print('Number of arguments:',str(len(sys.argv)),  'arguments.')
print('Argument List:', str(sys.argv))

def doit(op,wsize,inputfile,outputfile):
    print(op,wsize,inputfile,outputfile)
    with open(inputfile) as ifile:
        read_data = ifile.read()
        print("Leitura: ", read_data)


    # with open(inputfile,'r') as ifile:
    
    nameoutput = 'output/'
    if outputfile:
        nameoutput = nameoutput + outputfile + '.' + wsize + op
    else:
        nameoutput = nameoutput + inputfile.split('.')[0] + '.' + wsize + op
    
    with open(nameoutput, 'w') as ofile:
        print(read_data, file=ofile)


def main(argv):
    wordsize = ''
    inputfile = ''
    outputfile = ''
    mode = ''
    mainUsage = 'Usage:' + sys.argv[0] + '[-c | -d] -w <size> -i <inputfile> -o <outputfile>\nDetails:\n-h\t\tShow this message\n-c,-d\t\tOperation mode: -c (compression) or -d (decompression)\n-w\t\tWord size of compression/descompression\n-i\t\tInput file to compression/descompression\n-o\t\tOutput file (opcional)\n'
    try:
        opts, args = getopt.getopt(argv,"hcdw:i:o:",["wsize=","ifile=","ofile="])
    except getopt.GetoptError:
        print(mainUsage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(mainUsage)
            sys.exit()
        elif opt == '-d':
            mode = 'dec'
        elif opt == '-c':
            mode = 'com'
        elif opt in ("-w", "--wsize"):
            wordsize = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if mode and wordsize and inputfile:
        print('\n\t\tArgs are valid\n')
        doit(mode,wordsize,inputfile,outputfile)
    else:
        print('\n\t\tArgs are invalid\n')
        print(mainUsage)
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])



   """ temps1 = time.time()
    print("Tempo final: " + str(time.time() - temps1))
    
    operator.itemgetter(1)

    #gráficos
def graphEvolucaoMelhorAptidao(historico, senha):
	plt.axis([0,len(historico),0,105])
	plt.title(senha)
	evolucaoAptidao = []
	for populacao in historico:
		evolucaoAptidao.append(melhorIndividuoDaPopulacao(populacao, senha)[1])
	plt.plot(evolucaoAptidao)
	plt.ylabel('Melhor individuo Apto')
	plt.xlabel('Geracao')
	plt.show()

def graphEvolucaoAptidaoMediana(historico, senha, tam_populacao):
	plt.axis([0,len(historico),0,105])
	plt.title(senha)
	evolucaoAptidao = []
	for populacao in historico:
		populacaoAval = avaliarPopulacao(populacao, senha)
		aptidaoMediana = 0
		for individuo in populacaoAval:
			aptidaoMediana += individuo[1]
		evolucaoAptidao.append(aptidaoMediana/tam_populacao)
	plt.plot(evolucaoAptidao)
	plt.ylabel('Aptidao Mediana')
	plt.xlabel('Geracao')
	plt.show()
 """