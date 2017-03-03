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
    u_db = open('C10T8S8I8.txt', 'r')
    s_db = asciiFormater(u_db)
    ratio = 0.003
    options = {'threshold':int(math.ceil(len(s_db)*ratio))}
    print int(math.ceil(len(s_db)*ratio))
    print "GO!"
    start = time.time()
    res = ps.prefixspan(s_db, options)
    end = time.time()
    print len(res)
    print(end - start)
    out = open('Results','w')
    for pat in res:
        out.write(str(pat)+'\n')
    out.close()
    