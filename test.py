from multiprocessing import Process, Lock
# -*- coding: utf-8 -*-
import prefixspan as ps
import fileprocessor as fp
import time
import sys
import math
sys.setrecursionlimit(10000)

def experimentation(fEco, fRes, options):
    s_db, inttovar = fp.csvReader(fEco)
    res = ps.prefixspan(s_db, options)
    for pat in sorted(res, key=lambda x: len(x[0])):
        fRes.write(pat[0].extended_representation(lambda x: inttovar[x]).replace(' ','').replace('><', '>  <')+'\n')
    fRes.close()
    fEco.close()    

if __name__ == '__main__':
    fEco = open('D:\AsteriskAmpersand\Documents\GitHub\Windowed-Copper\Lazo\DiscAmericanBanks.csv', 'r')
    fRes = open('D:\AsteriskAmpersand\Documents\GitHub\Windowed-Copper\Lazo\ABank_t5g0w4mss3.txt', 'w')
    options = {'threshold': 5, 'gap': 0, 'window': 4, 'minSseq': 3}
    experimentation(fEco, fRes, options)
    print options

    fEco = open('D:\AsteriskAmpersand\Documents\GitHub\Windowed-Copper\Lazo\DiscAmericanBanks.csv', 'r')
    fRes = open('D:\AsteriskAmpersand\Documents\GitHub\Windowed-Copper\Lazo\ABank_t5g1w6mss2ms2.txt', 'w')
    options = {'threshold': 5, 'gap': 1, 'window': 6, 'minSseq':2 , 'minSize': 2}
    experimentation(fEco, fRes, options)
    print options

    fEco = open('D:\AsteriskAmpersand\Documents\GitHub\Windowed-Copper\Lazo\DiscAmericanBanks.csv', 'r')
    fRes = open('D:\AsteriskAmpersand\Documents\GitHub\Windowed-Copper\Lazo\ABank_t4g0w4mss3.txt', 'w')
    options = {'threshold': 4, 'gap': 0, 'window': 4, 'minSseq': 3}
    experimentation(fEco, fRes, options)
    print options

##    fEco = open('D:\AsteriskAmpersand\Documents\GitHub\Windowed-Copper\Lazo\DiscAmericanBanks.csv', 'r')
##    fRes = open('D:\AsteriskAmpersand\Documents\GitHub\Windowed-Copper\Lazo\ABank_t4g1w6mss2ms3.txt', 'w')
##    options = {'threshold': 4, 'gap': 1, 'window': 4, 'minSseq':2 , 'minSize': 3}
##    experimentation(fEco, fRes, options)
##    print options
