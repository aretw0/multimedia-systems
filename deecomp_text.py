import getopt
import os
import sys
import time
import plotly.plotly as py
import plotly.graph_objs as go

deecomp_config = {
    'inpf': '',
    'outpf': '',
    'orig_size': 0,
    'alg': 'rule',
    'mode': 'com',
    'w_size': '2'
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
        # workdata = data#.hex()
        temps1 = time.time()
        # do something
        datalen = len(data)
        word = data[0:wsize]
        tvalue = 1
        lword = ''
        for k in range(0,datalen,wsize):
            tword = data[k:k+wsize]
            # print(tword)
            if tword == word:
                if k:
                    tvalue += 1
            else:       
                if tvalue == 1 and k:
                    tlen = len(word)
                    if tlen < wsize:
                        tvalue = tlen - wsize
                        for t in range(wsize-tlen):
                            word += '*'
                if lword:
                    lword += ';'
                lword += str(tvalue) + '/' + word        
                word = tword
                tvalue = 1
        if tvalue == 1 and k:
            tlen = len(word)
            if tlen < wsize:
                tvalue = tlen - wsize
                for t in range(wsize-tlen):
                    word += '*'
        lword += ';' + str(tvalue) + '/' + word     
        
        algs['rule']['timec'] = time.time() - temps1
        finaldata = lword     
    else:
        # print("Preparar dados para run-length")
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

        # finaldata = bytes.fromhex(tempdata)
        algs['rule']['timed'] = time.time() - temps1
        finaldata = tempdata
    
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

        algs['huff']['time'] = time.time() - temps1
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
        'dec': ''
    },

    'shfe': {
        'fn': _shfe,
        'use': False,
        'timec': 0,
        'timed': 0,
        'size': 0,
        'com': '',
        'compress_ratio': 0,
        'dec': ''
    },

    'huff': {
        'fn': _huff,
        'use': False,
        'timec': 0,
        'timed': 0,
        'size': 0,
        'com': '',
        'compress_ratio': 0,
        'dec': ''
    }
    
}

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
        title=alg.upper() + ' Compression results',
    )
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='color-bar_'+infoChart)

def comparestats():
    print("Irei mostrar stats das operacoes")

def breakdown():
    
    inputf = deecomp_config['inpf']
    outputf = deecomp_config['outpf']
    mode = deecomp_config['mode']
    alg = deecomp_config['alg']
    wsize = deecomp_config['w_size']

    deecomp_config['orig_size'] = orig_size = os.stat(inputf).st_size

    with open(inputf) as ifile:
        read_data = ifile.read()

    algs[alg]['fn'](mode,wsize,read_data)

    for k in algs:
        if k != 'all':
            if algs[k]['use']:
                nameout = name_out(k,mode,wsize,inputf,outputf)
                with open(nameout,'w') as ofile:
                    ofile.write(algs[k][mode])
                if mode == 'com':
                    algs[k]['size'] = comp_size = os.stat(nameout).st_size
                    algs[k]['compress_ratio'] = ((float(orig_size) - float(comp_size)) / float(orig_size))
                    showstats(k)
                benchmark(k,mode)
    if alg == 'all' and mode == 'comp':
        comparestats()
    
    print("Finish!")


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
            print(k,v)
        print()
        breakdown()
    else:
        print('\n\t\tArgs are invalid\n')
        print(mainUsage)
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
