import getopt
import os
import sys
import time
import plotly.graph_objs as go
import plotly.plotly as py

# print('Number of arguments:',str(len(sys.argv)),  'arguments.')
# print('Argument List:', str(sys.argv))
# todo salvar em binario, limitar o rule (alg)

deecomp_config = {
    'inpf': '', # input/lena.bmp
    'outpf': '',
    'orig_size': 0,
    'alg': '',
    'mode': '',
    'w_size': ''
}

openmode = {
    'read' : {
        'com' : 'rb',
        'dec' : 'r'
    },
    'write' : {
        'com' : 'w',
        'dec' : 'wb'
    }
}

def _all(mode,wsize,data):
    print("All alg")
    _rule(mode,wsize,data)
    _shfe(mode,wsize,data)
    _huff(mode,wsize,data)

def _rule(mode,wsize,data):
    print("Run-Length alg")
    algs['rule']['use'] = True
    if mode == 'com':
        workdata = data.hex()
        
        
        word = workdata[0]
        lword = ''
        tvalue = 0
        s_count = wsize - 8 # retirando os bits para a letra
        temps1 = time.time()
        # do something
        for ch in workdata:
            if ch == word:
                if tvalue < s_count:
                    tvalue += 1
                else:
                    # if s_count > 3 and tvalue < 10:
                    #     lword += '0'
                    lword += str(tvalue) + word
                    tvalue = 0
            else:
                lword += str(tvalue) + word
                word = ch
                tvalue = 0
        
        lword += str(tvalue) + ch
        
        algs['rule']['timec'] = time.time() - temps1
        finaldata = lword        
    else:
        temps1 = time.time()
        tempdata = ''
        for k in data.split(';'):
            tvalue = k.split('/')
            tint = int(tvalue[0])
            for v in range(tint):
                # print(tvalue[1])
                tempdata += tvalue[1]
            else:
                if tint < 0:
                    tempdata += tvalue[1].replace((tint*-1)*"*",'')
        
        algs['rule']['timed'] = time.time() - temps1
        finaldata = bytes.fromhex(tempdata)
        # finaldata = tempdata
    
    algs['rule'][mode] = finaldata

def _shfe(mode,wsize,data):
    print("Shannon-Feno alg")
    algs['shfe']['use'] = True

    if mode == 'com':
        workdata = data.hex()
        temps1 = time.time()
        # do something

        algs['shfe']['timec'] = time.time() - temps1
    else:
        print("Preparar dados para shannon-feno")
        # finaldata = bytes.fromhex(tempdata)
    
    # algs['shfe'][mode] = finaldata


def _huff(mode,wsize,data):
    print("Huffman alg")
    algs['huff']['use'] = True
    
    if mode == 'com':
        workdata = data.hex()
        temps1 = time.time()
        # do something

        algs['huff']['timec'] = time.time() - temps1
    else:
        print("Preparar dados para huffman")
        # finaldata = bytes.fromhex(tempdata)

    # algs['huff'][mode] = finaldata


algs = {
    'all' : _all,
    'rule': {
        'fn':_rule,
        'use': False,
        'timec': 0,
        'timed': 0,
        'size': 0,
        'com': '',
        'compress_ratio': 0,
        'dec': b''
    },

    'shfe': {
        'fn': _shfe,
        'use': False,
        'timec': 0,
        'timed': 0,
        'size': 0,
        'com': '',
        'compress_ratio': 0,
        'dec': b''
    },

    'huff': {
        'fn': _huff,
        'use': False,
        'timec': 0,
        'timed': 0,
        'size': 0,
        'com': '',
        'compress_ratio': 0,
        'dec': b''
    }
    
}
def benchmark(alg,mode):
    print("\nAlgorithm ("+mode.upper()+"):\t",alg.upper(),'\n')
    if mode == 'com':
        print("Compressed:\t\t%d%%\n" % (100.0 * algs[alg]['compress_ratio']))
        print("Time:\t\t",algs[alg]['timec'],"\n")
    else:
        print("Time:\t\t",algs[alg]['timed'],"\n")

def showstats(alg):
    
    inpf = deecomp_config['inpf']
    inpfs = inpf.split('/')
    infoChart = alg + '_'+str(deecomp_config['w_size'])+ '_' + inpfs[len(inpfs)-1]

    orig_size = deecomp_config['orig_size']
    new_size = algs[alg]['size']
    saved = orig_size-new_size
    if saved <= 0:
        labelsPie = ['Original','Adicional']
        valuesPie = [orig_size,new_size-orig_size]
        
    else:
        labelsPie = ['Saved','Compressed']
        valuesPie = [saved,orig_size-saved]
    
    trace = go.Pie(labels=labelsPie, values=valuesPie)
    py.iplot([trace], filename='piechart_'+infoChart)
    
    labelsBar = ['Original','Final']
    valuesBar = [orig_size,new_size]

    trace0 = go.Bar(
        x=labelsBar,
        y=valuesBar,
        marker=dict(
            color=['rgba(204,204,204,1)', 'rgba(222,45,38,0.8)']
        )
    )
    data = [trace0]
    layout = go.Layout(
        title='Compression results',
    )
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='color-bar_'+infoChart)

def comparestats():
    print("Irei mostrar stats das operações")

def name_out(alg,mode,wsize,inputf,outputf):
    inputsplit = inputf.split('.')
    nameoutput = 'output'+'_'+ mode +'/'
    if outputf:
        nameoutput += outputf + '.' + inputsplit[1]
    else:
        tip = inputsplit[0].split('/')
        nameoutput += tip[len(tip)-1] + '.' + inputsplit[1]
    if mode == 'com':
        nameoutput += '.' + alg + str(wsize)
    return nameoutput

def breakdown():
    
    inputf = deecomp_config['inpf']
    outputf = deecomp_config['outpf']
    mode = deecomp_config['mode']
    alg = deecomp_config['alg']
    wsize = deecomp_config['w_size']

    deecomp_config['orig_size'] = orig_size = os.stat(inputf).st_size

    with open(inputf,'rb') as ifile:
        read_data = ifile.read()

    algs[alg]['fn'](mode,wsize,read_data)

    for k in algs:
        if k != 'all':
            if algs[k]['use']:
                nameout = name_out(k,mode,wsize,inputf,outputf)
                with open(nameout,'wb') as ofile:
                    ofile.write(algs[k][mode].encode())
                if mode == 'com':
                    algs[k]['size'] = comp_size = os.stat(nameout).st_size
                    algs[k]['compress_ratio'] = compress_ratio = ((float(orig_size) - float(comp_size)) / float(orig_size))
                    showstats(k)
                benchmark(k,mode)
    if alg == 'all' and mode == 'comp':
        comparestats()



# http://nen-file.azurewebsites.net/ usar para comparar


def main(argv):
    mainUsage = 'Usage: ' + sys.argv[0] + ' -m <mode> -a <alg> -w <size> -i <inputfile> -o <outputfile>\nDetails:\n-h\t\tShow this message\n-m\t\tMode: com (Compression) or dec (Decompression\n-a\t\tAlgorithm (opcional for compression): rule, huff or shfe\n-w\t\tWord size of compression/descompression\n-i\t\tInput file to compression/descompression\n-o\t\tOutput file (opcional)\n'
    try:
        opts, args = getopt.getopt(argv,"hm:a:w:i:o:",["alg=","mode=","wsize=","ifile=","ofile="])
    except getopt.GetoptError:
        print(mainUsage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(mainUsage)
            sys.exit()
        elif opt in ("-a","--alg"):
            if arg == "rule" or arg == "shfe" or arg == "huff" or arg == "all":
                deecomp_config['alg'] = arg
            elif arg:
                print("Oops!",arg,"was no valid algorithm.  Try again...")
                sys.exit(2)
            else:
                deecomp_config['alg'] = 'all'
        elif opt in ('-m',"--mode"):
            if arg == "com" or arg == "dec":
                deecomp_config['mode'] = arg
            else:
                print("Oops!",arg,"was no valid mode.  Try again...\n")
                sys.exit(2)
        elif opt in ("-w", "--wsize"):
            try:
                deecomp_config['w_size'] = arge = int(arg)
            except ValueError:
                print("Oops!",arg,"was no valid word size number.  Try again...")
                sys.exit(2)
        elif opt in ("-i", "--ifile"):
            deecomp_config['inpf'] = arg
        elif opt in ("-o", "--ofile"):
             deecomp_config['outpf'] = arg

    if deecomp_config['mode'] == 'dec' and (not deecomp_config['alg'] or deecomp_config['alg'] == 'all'):
        print("Oops! Needed algorithm for descompression.  Try again...\n")
        sys.exit(2)
    
    if deecomp_config['mode'] and deecomp_config['inpf']:
        print('\n\t\tArgs are valid\n')
        for k,v in deecomp_config.items():
            print(v)
        breakdown()
    else:
        print('\n\t\tArgs are invalid\n')
        print(mainUsage)
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])

# breakdown()