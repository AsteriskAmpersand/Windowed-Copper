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
