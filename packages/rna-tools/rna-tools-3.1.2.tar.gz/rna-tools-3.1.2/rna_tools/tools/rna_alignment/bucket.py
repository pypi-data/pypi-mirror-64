    # manage pseudoknots
def x():
    ssl = list(nss)

    pseudoknots = {'A': {'left':'[', 'right':']'},
                   'B': {'left':'{', 'right':'}'},
                   'C': {'left':'<', 'right':'>'},}

    for pseudoknot in pseudoknots:
        pklen = (ssl.count(pseudoknot) / 2)  # to get AAA AAA to get cut middle point to switch
        # from left to right

        if pklen:  # if pk of given type is detected, then run this
            pkindex = 0
            for c, nt in enumerate(ssl):  # s
                #print(nt, pkindex)
                if nt == 'A':
                    if pkindex > (pklen / 2):
                        ssl[c] = pseudoknots[pseudoknot]['right']
                    else:
                        ssl[c] = pseudoknots[pseudoknot]['left']
                    pkindex += 1



    print(xx)
    record = SeqRecord(Seq('-' * 82), id="YP_025292.1", name="HokC", description="toxic membrane protein, small")
    print(record)

    a.append(record)
    print(a)
    AlignIO.write(a, 'a.sto', 'stockholm')
