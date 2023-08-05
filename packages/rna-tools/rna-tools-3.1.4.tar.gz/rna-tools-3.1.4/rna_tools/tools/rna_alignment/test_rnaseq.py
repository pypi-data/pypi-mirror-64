import rna_alignment as ra

if __name__ == '__main__':
    a = ra.RNAalignment('../../input/RF02679_pistol_stockholm.txt')
    print(a)
    print(a.ss_cons_std)
    for s in a:
        print('----------------------------')
        print(s.seq)
        print(s.ss)
        s.remove_gaps()
        print(s.seq)
        print(s.ss)
