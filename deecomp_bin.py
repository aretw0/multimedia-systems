import getopt
import os
import sys
import time
import hashlib
# import plotly.graph_objs as go
# import plotly.plotly as py

# print('Number of arguments:',str(len(sys.argv)),  'arguments.')
# print('Argument List:', str(sys.argv))
# todo salvar em binario, limitar o rule (alg)

deecomp_config = {
    'inpf': 'input/lena.bmp', # input/lena.bmp
    'outpf': '',
    'orig_size': 0,
    'alg': 'rule',
    'mode': 'com',
    'w_size': 11,
    'check_sum': '',
    'bitStream': '',
    'bitPosition' : 0
}

openmode = {
    'read' : {
        'com' : 'rb',
        'dec' : 'rb'
    },
    'write' : {
        'com' : 'wb',
        'dec' : 'wb'
    }
}

def sha256(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def shannon_fano_encoder(iA, iB): # iA - iB : intervalo
    size = iB - iA + 1
    if size > 1:
        # Divide a lista em 2 groups.
        # Grupo melhor levar 0, pior 1 como novo bit de econding
        mid = int(size / 2 + iA)
        tupleList = algs['shfe']['tupleList']
        for i in range(iA, iB + 1):
            tup = tupleList[i]
            if i < mid: # top group
                tupleList[i] = (tup[0], tup[1], tup[2] + '0')
            else: # bottom group
                tupleList[i] = (tup[0], tup[1], tup[2] + '1')
        # do recursive calls for both groups
        algs['shfe']['tupleList'] = tupleList
        shannon_fano_encoder(iA, mid - 1)
        shannon_fano_encoder(mid, iB)

def byteWriter(bitStr,fdata):
    deecomp_config['bitStream'] += bitStr
    bitStream = deecomp_config['bitStream']
    while len(bitStream) > 8: # write byte(s) if there are more then 8 bits
        byteStr = bitStream[:8]
        bitStream = bitStream[8:]
        fdata += bytes([(int(byteStr, 2))])
    deecomp_config['bitStream'] = bitStream
    return fdata

def bitReader(n,byteArr): # number of bits to read
    bitStr = ''
    bitPosition = deecomp_config['bitPosition']
    for i in range(n):
        bitPosInByte = 7 - (bitPosition % 8)
        bytePosition = int(bitPosition / 8)
        byteVal = byteArr[bytePosition]
        bitVal = int(byteVal / (2 ** bitPosInByte)) % 2
        bitStr += str(bitVal)
        bitPosition += 1 # prepare to read the next bit
    deecomp_config['bitPosition'] = bitPosition
    return bitStr

def _all(mode,wsize,data):
    print("All alg")
    _rule(mode,data)
    _shfe(mode,data)
    _huff(mode,data)

def _rule(mode,data):
    print("Run-Length alg")
    algs['rule']['use'] = True
    if mode == 'com':
        # workdata = data.hex()
        # word = workdata[0:1]
        word = data[0]
        lword = b""
        # lword = ""
        tvalue = -1
        temps1 = time.time()
        # do something
        for b in range(len(data)):
            if data[b] == word:
                if tvalue < 256:
                    tvalue += 1
                else:
                    lword += bytes(chr(tvalue),'utf-8') + data[b:b+1]
                    tvalue = 0
            else:
                if tvalue < 0:
                    tvalue = 0
                lword += bytes(chr(tvalue),'utf-8') + data[b-1:b]
                tvalue = 0
                word = data[b]
        
        lword += bytes(chr(tvalue),'utf-8') + data[b:b+1]
        
        algs['rule']['timec'] = time.time() - temps1
        finaldata = lword        
    else:
        temps1 = time.time()
        lword = b""
        for b in range(0,len(data)-1,2):
            tvalue = data[b]
            for v in range(tvalue+1):
                lword += data[b+1:b+2]
        
        algs['rule']['timed'] = time.time() - temps1
        finaldata = lword
        # finaldata = tempdata
    
    algs['rule'][mode] = finaldata

def _shfe(mode,data):
    print("Shannon-Feno alg")
    algs['shfe']['use'] = True

    if mode == 'com':
        temps1 = time.time()
        finaldata = b''
        # do something
         # calcular a frequencia de cada byte no arquivo
        freqList = [0] * 256 
        for b in data:
            freqList[b] += 1
        # cria uma lista de (frequency, byteValue, encodingBitStr) tuplas
        tupleList = []
        for b in range(256):
            if freqList[b] > 0:
                tupleList.append((freqList[b], b, ''))
        # organiza a lista pela maior frequencia a menor freq
        algs['shfe']['tupleList'] = sorted(tupleList, key=lambda tup: tup[0], reverse = True)

        shannon_fano_encoder(0, len(algs['shfe']['tupleList']) - 1)
        
        # cria um dicionário com pares de byteValue : encodingBitStr
        dic = dict([(tup[1], tup[2]) for tup in algs['shfe']['tupleList']])
        
        deecomp_config['bitStream'] = ''

        # quantos bytes precisamos pra salvar a quantidade de tuplas?
        qt = 0
        tdic = len(dic) - 1
        qbdic = 0
        for t in range(0,tdic,255):
            if t:
                qt += 255
                qbdic +=1
        towrite = [qbdic,tdic-qt]
        for q in range(qbdic):
            towrite.append(255)
        print("Why?")
        finaldata += bytes(towrite)

        for (byteValue, encodingBitStr) in dic.items():
            # convert the byteValue into 8-bit and send to be written into file
            # finaldata += bytes([byteValue])
            # bitStr = bin(byteValue)
            # bitStr = bitStr[2:] # remove 0b
            # bitStr = '0' * (8 - len(bitStr)) + bitStr # add 0's if needed for 8 bits
            # finaldata = byteWriter(bitStr,finaldata)
            finaldata += bytes([byteValue])
            # convert len(encodingBitStr) to 3-bit and send to be written into file
            # bitStr = bin(len(encodingBitStr) - 1) # 0 a 111
            # bitStr = bitStr[2:] # remove 0b
            # bitStr = '0' * (3 - len(bitStr)) + bitStr # add 0's if needed for 3 bits
            # finaldata = byteWriter(bitStr,finaldata)
            finaldata += bytes([len(encodingBitStr) - 1])
            # send encodingBitStr to be written into file
            # finaldata = byteWriter(encodingBitStr,finaldata)
            finaldata += bytes([int(encodingBitStr,2)])
         # write 32-bit (input file size)-1 value
        # bitStr = bin(deecomp_config['orig_size'] - 1)
        # bitStr = bitStr[2:] # remove 0b
        # bitStr = '0' * (32 - len(bitStr)) + bitStr # add 0's if needed for 32 bits
        # finaldata = byteWriter(bitStr,finaldata)

        # write the encoded data
        for b in data:
            # finaldata = byteWriter(dic[b], finaldata)
            finaldata += bytes([int(dic[b],2)])

        # finaldata = byteWriter('0' * 8, finaldata) # to write the last remaining bits (if any)
        algs['shfe']['timec'] = time.time() - temps1
    else:
        print("Preparar dados para shannon-feno")
        # finaldata = bytes.fromhex(tempdata)
        deecomp_config['bitPosition'] = 0
        bnt = data[0] + 1
        nt = 0
        if bnt > 1:
            for i in range(1,bnt):
                nt += data[i] + 1
            deecomp_config['bitPosition'] = i
        else:
            nt = data[1]
            deecomp_config['bitPosition'] = 1
        dic = dict()
        bitPos = deecomp_config['bitPosition']
        for i in range(nt+1):
            # byteValue = int(bitReader(8,data), 2)
            byteValue = data[bitPos+i+1]
            m = data[bitPos+i+2] + 1
            # m = int(bitReader(3,data), 2) + 1
            # encodingBitStr = bitReader(m,data)
            # encodingBitStr = bin(data[bitPos+i+2])[2:]
            # if len(encodingBitStr) < m:
            #     encodingBitStr += ("0" * m) + encodingBitStr
            encond = data[bitPos+i+3]
            dic[str(encond)] = byteValue
        deecomp_config['bitPosition'] = 8*(i+2+bitPos)
        # read the encoded data, decode it, write into the output file
        finaldata = bytes()
        bitPos = deecomp_config['bitPosition']
        for b in range(i,len(data[i:])):
            finaldata += bytes([dic[str(data[b])]])
        # read bits until a decoding match is found

            # encodingBitStr = ''
            # while True:
            #     encodingBitStr += bitReader(1,data)
            #     if encodingBitStr in dic:
            #         byteValue = dic[encodingBitStr]
            #         finaldata += bytes([byteValue])
            #         break
        
    algs['shfe'][mode] = finaldata


def _huff(mode,data):
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
        'dec': b'',
        'tupleList': []
    },

    'huff': {
        'fn': _huff,
        'use': False,
        'timec': 0,
        'timed': 0,
        'size': 0,
        'com': '',
        'compress_ratio': 0,
        'dec': b'',
        'tupleList': []
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
    infoChart = alg + '_' + inpfs[len(inpfs)-1]

    orig_size = deecomp_config['orig_size']
    new_size = algs[alg]['size']
    saved = orig_size-new_size
    if saved <= 0:
        labelsPie = ['Original','Adicional']
        valuesPie = [orig_size,new_size-orig_size]
        
    else:
        labelsPie = ['Saved','Compressed']
        valuesPie = [saved,orig_size-saved]
    
    # trace = go.Pie(labels=labelsPie, values=valuesPie)
    # py.iplot([trace], filename='piechart_'+infoChart)
    
    # labelsBar = ['Original','Final']
    # valuesBar = [orig_size,new_size]

    # trace0 = go.Bar(
    #     x=labelsBar,
    #     y=valuesBar,
    #     marker=dict(
    #         color=['rgba(204,204,204,1)', 'rgba(222,45,38,0.8)']
    #     )
    # )
    # data = [trace0]
    # layout = go.Layout(
    #     title='Compression results',
    # )
    # fig = go.Figure(data=data, layout=layout)
    # py.iplot(fig, filename='color-bar_'+infoChart)

def comparestats():
    print("Irei mostrar stats das operações")

def name_out(alg,mode,inputf,outputf):
    inputsplit = inputf.split('.')
    nameoutput = 'output'+'_'+ mode +'/'
    if outputf:
        nameoutput += outputf + '.' + inputsplit[1]
    else:
        tip = inputsplit[0].split('/')
        nameoutput += tip[len(tip)-1] + '.' + inputsplit[1]
    if mode == 'com':
        nameoutput += '.' + alg
    return nameoutput

def breakdown():
    
    inputf = deecomp_config['inpf']
    outputf = deecomp_config['outpf']
    mode = deecomp_config['mode']
    alg = deecomp_config['alg']

    deecomp_config['orig_size'] = orig_size = os.stat(inputf).st_size
    
    if mode == 'com':
        deecomp_config['check_sum'] = sha256(inputf)
        if deecomp_config['check_sum'] != sha256(inputf):
            print("Bitch are you kidding me?")
        else:
            print("Ok ne")

    with open(inputf,'rb') as ifile:
        read_data = ifile.read()

    algs[alg]['fn'](mode,read_data)
    nameout = ""
    for k in algs:
        if k != 'all':
            if algs[k]['use']:
                nameout = name_out(k,mode,inputf,outputf)
                with open(nameout,'wb') as ofile:
                    ofile.write(algs[k][mode])
                if mode == 'com':
                    algs[k]['size'] = comp_size = os.stat(nameout).st_size
                    algs[k]['compress_ratio'] = compress_ratio = ((float(orig_size) - float(comp_size)) / float(orig_size))
                    with open(nameout,'rb') as pfile:
                        proofdata = pfile.read()
                    algs[k]['fn']('dec',proofdata)
                    namedec = name_out(k,'dec',nameout,outputf)
                    with open(namedec,'wb') as ofile:
                        ofile.write(algs[k]['dec'])
                    if deecomp_config['check_sum'] == sha256(namedec):
                        print("On",k.upper(),"Files are identical!")
                    else:
                        print("On",k.upper(),"Files are not identical!")
                    showstats(k)
                    
                benchmark(k,mode)

    if alg == 'all' and mode == 'com':
        comparestats()



# http://nen-file.azurewebsites.net/ usar para comparar


def main(argv):
    mainUsage = 'Usage: ' + sys.argv[0] + ' -m <mode> -a <alg> -i <inputfile> -o <outputfile>\nDetails:\n-h\t\tShow this message\n-m\t\tMode: com (Compression) or dec (Decompression\n-a\t\tAlgorithm (opcional for compression): rule, huff or shfe\n-i\t\tInput file to compression/descompression\n-o\t\tOutput file (opcional)\n'
    try:
        opts, args = getopt.getopt(argv,"hm:a:i:o:",["alg=","mode=","ifile=","ofile="])
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