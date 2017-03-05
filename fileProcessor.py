"""
Implementation of Jiawei Han, Jian Pei, Behzad Mortazavi-Asl, Helen Pinto, Qiming Chen, Umeshwar Dayal, MC Hsu, Prefixspan Algorithm (http://jayurbain.com/msoe/cs498-datamining/prefixspan_mining_sequential_patterns_by_prefix_projected_growth.pdf) in Python.
With additional capabilities added from Guevara-Cogorno, Flamand, Alatrista Salas, COPPER Paper (http://www.sciencedirect.com/science/article/pii/S1877050915024990)
and Window/Time Gap Capabilities added.

Author: Agustin Guevara-Cogorno
Contact Details: a.guevarac@up.edu.pe
Institution: Universidad del Pacifico|University of the Pacific
"""

def unsafeJoin(x, base=''):
    string = base
    for i in x:
        string+=i
    return string

def asciiFormater(asciiFile):
    pDB = []
    for index, line in enumerate(asciiFile):
        pattern = []
        itemset = ''
        splitLine = line.replace(' \n','').split(' ')
        ignore = True
        first = True
        counter = 0
        for slot in splitLine:
            if not ignore:
                if not counter:
                    counter = int(slot)
                    if first:
                        first = False
                    else:
                        pattern.append(itemset[:-1]+'\0')
                        itemset = ''
                else:
                    counter -= 1
                    itemset+=slot+'|'
            else:
                ignore = False
        pDB.append((str(index)+ unsafeJoin(pattern,'\0'))[:-1] )
    return pDB

def asciiToMinOne(asciiFile):
    pDB = []
    for index, line in enumerate(asciiFile):
        pattern = []
        itemset = ''
        splitLine = line.replace(' \n','').split(' ')
        ignore = True
        first = True
        counter = 0
        for slot in splitLine:
            if not ignore:
                if not counter:
                    counter = int(slot)
                    if first:
                        first = False
                    else:
                        pattern.append(itemset[:-1]+' -1 ')
                        itemset = ''
                else:
                    counter -= 1
                    itemset+=slot+' '
            else:
                ignore = False
        pDB.append(((str(1)+ unsafeJoin(pattern,''))[:-1] + '-2')[1:])
    return pDB    
    
def minOneFormater(moDB):
    patternDB = []
    for line, entry in enumerate(moDB):
        splitted = entry.rstrip().replace("-1","\0").replace("-2","").split('\0')[:-1]
        patternDB.append(str(line)+unsafeJoin(map(lambda x: x.lstrip().rstrip().replace(' ','|')+"\0", splitted),'\0')[:-1])
    return patternDB

import prefixspan as ps
import time
import sys
import math
sys.setrecursionlimit(10000)

if __name__ == '__main__':
    u_db = open('C01T5S250I003SP5.txt', 'r')#C10T8S8I8
    s_db = asciiFormater(u_db)
    ratio = 0.75#0.003
    options = {'threshold':int(math.ceil(len(s_db)*ratio)), 'gap':2, 'window':10}
    string = '' if 'window' not in options else 'Window'
    string += '' if 'gap' not in options else 'Gap'
    print "Min Support: "+str(int(math.ceil(len(s_db)*ratio)))
    start = time.time()
    res = ps.prefixspan(s_db, options)
    end = time.time()
    print "Patterns Found: " + str(len(res))
    print "Time Taken: " + str(end - start)
    out = open('Results'+string+'.txt','w')
    for pat in sorted(res, key=lambda x: x[1]):
        out.write(str(pat)+'\n')
    out.close()
    print "Options Used: " + str(options)
    
