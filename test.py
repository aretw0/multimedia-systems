


 # datalen = len(workdata)
        # word = workdata[0:wsize]
        # tvalue = 1
        
        # for k in range(0,datalen,wsize):
        #     tword = workdata[k:k+wsize]
        #     # print(tword)
        #     if tword == word:
        #         if k:
        #             tvalue += 1
        #     else:       
        #         if tvalue == 1 and k:
        #             tlen = len(word)
        #             if tlen < wsize:
        #                 tvalue = tlen - wsize
        #                 for t in range(wsize-tlen):
        #                     word += '*'
        #         if lword:
        #             lword += ';'
        #         lword += str(tvalue) + '/' + word        
        #         word = tword
        #         tvalue = 1
        # if tvalue == 1 and k:
        #     tlen = len(word)
        #     if tlen < wsize:
        #         tvalue = tlen - wsize
        #         for t in range(wsize-tlen):
        #             word += '*'
        # lword += ';' + str(tvalue) + '/' + word     