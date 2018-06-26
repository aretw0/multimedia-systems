# import hashlib

# def sha256(fname):
#     hash_sha256 = hashlib.sha256()
#     with open(fname, "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_sha256.update(chunk)
#     return hash_sha256.hexdigest()


# wsize = 11

# sha = sha256('input/texto.txt')

# with open('input/lena.bmp','rb') as ifile:
#         data = ifile.read()
# print('ouu')
# word = data[0]
# # testeando = data.decode('base64_codec')
# tvalue = -1
# lword = b''
# s_count = pow(2,(wsize - 8)) - 1 # retirando os bits para a letra
# # do something
# for b in range(len(data)):
#         # print(type(b))
#         if data[b] == word:
#                 if tvalue < 256:
#                         tvalue += 1
#                 else:
#                         lword += bytes(chr(tvalue),'utf-8') + data[b:b+1]
#                         tvalue = 0
#         else:
#                 if tvalue < 0:
#                         tvalue = 0
#                 lword += bytes(chr(tvalue),'utf-8') + data[b-1:b]
#                 tvalue = 0
#                 word = data[b]
        
# lword += bytes(chr(tvalue),'utf-8') + data[b:b+1]


#lword contem meus dados em binário
# with open('output_com/texto.txt.rule11','wb') as ofile:
#         ofile.write(lword)

# with open('input/texto1.txt','wb') as ofile:
#         ofile.write(data)

# if sha == sha256('input/texto1.txt'):
#         print("Files are identical")
# else:
#         print("Files are not identical")

# utu = 7
# uta = bytes([utu])
# print("ouo")

# print(bytes(bin(utu)[2:],'utf-8'))



qt = 0
tdic = 257 - 1
qbdic = 0
for t in range(0,tdic,255):
    if t:
        qt += 255
        qbdic +=1
towrite = [qbdic,tdic-qt]
for d in range(qbdic):
    towrite.append(255)

utu = bytes(towrite)
print(utu)
print("uou")