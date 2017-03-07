"""
Implementation of Jiawei Han, Jian Pei, Behzad Mortazavi-Asl, Helen Pinto, Qiming Chen, Umeshwar Dayal, MC Hsu, Prefixspan Algorithm (http://jayurbain.com/msoe/cs498-datamining/prefixspan_mining_sequential_patterns_by_prefix_projected_growth.pdf) in Python.
With additional capabilities added from Guevara-Cogorno, Flamand, Alatrista Salas, COPPER Paper (http://www.sciencedirect.com/science/article/pii/S1877050915024990)
and Window/Time Gap Capabilities added.

Author: Agustin Guevara-Cogorno
Contact Details: a.guevarac@up.edu.pe
Institution: Universidad del Pacifico|University of the Pacific
"""
from seqpattern import Pattern
from dbpointer import DBPointer, CopperPointer, WindowGapPointer, WinCopPointer
from infinity import Infinity
import logiceval

def __parse_db__(db):
    """Takes a list of strings in the expected format and parses them into the db, a converter from zone to zone_id
        and a frequency dictionary each item on the database"""
    zone2int = {}
    parseddb = []
    itembag={}
    for line in db:
        sequencebag=set()
        sequence = []
        i = line.split('\0')
        if i[0] not in zone2int:
            zone2int[i[0]]=len(zone2int)
        for itemset in i[1:]:
            iset = set()#!
            for item in itemset.split('|'):
                if item:
                    sequencebag.add(int(item))
                    iset.add(int(item))
            sequence.append(iset)
        parseddb.append(sequence)
        for item in sequencebag:
            if item in itembag:
                itembag[item]+=1
            else:
                itembag[item]=1
    return parseddb, zone2int, itembag

def __parse_options__(options):
    """Parses options and checks the minimum set of options is present. Selects the correct classes for each version of the algorithm."""
    assert 'threshold' in options
    assert isinstance( options['threshold'], ( int, long ) )
    #Standard prefixspan
    options['Pattern'] = Pattern
    options['DBPointer'] = DBPointer
    #COPPER
    if any( param in options for param in ['logic', 'minSseq','maxSseq','minSize','maxSize']):
        options['DBPointer'] = CopperPointer
        if 'logic' not in options:
            options['logic'] = lambda x: True
        else:
            options['logic'] = logiceval.evaluator(options['logic'])
        if 'minSseq' not in options:
            options['minSseq'] = 0
        if 'maxSseq' not in options:
            options['maxSseq'] = Infinity()
        if 'minSize' not in options:
            options['minSize'] = 0
        if 'maxSize' not in options:
            options['maxSize'] = Infinity()
    #Window
    if any( param in options for param in ['window','gap']):
        options['DBPointer'] = WindowGapPointer
        if 'gap' in options:
            gap = options['gap']+1
            options['gap'] = lambda x, y: map(lambda z: [z+1, min(z+gap+1, y)], x)
        else:
            options['gap'] = lambda x, y: [[x[0]+1, y]]
        if 'window' in options:
            window = options['window']
            options['window'] = lambda x, y: map(lambda z: [z+1, min(z+window+1, y)], x)
        else:
            options['window'] = lambda x, y: [[0, y]]
    #WinCopper
    if 'logic' in options and 'gap' in options:
        options['DBPointer'] = WinCopPointer
    return options

def __ffi__(support, itembag):
    """Returns frequent items from the itembag given support and itembag"""
    return [i for i in itembag if itembag[i]>=support]

def __itembag_merge__(itembaglist):
    """Merges Multiple itembags while keeping count in how many a given item appears"""
    mergedbag = {}
    for bag in itembaglist:
        for item in bag:
            if item in mergedbag:
                mergedbag[item]+=1
            else:
                mergedbag[item]=1
    return mergedbag

def __prefixspan__(u_pointerdb, u_pattern, options, freqpatterns):
    """Prefixspan proper recursive call"""
    #Projection
    pointerdb = []
    for entry in (entry.project(u_pattern, options) for entry in u_pointerdb):   
        if entry:                                                       
            pointerdb.append(entry)
    freqpatterns.append([u_pattern, len(pointerdb)])
    #Assemble - Get assemble candidates
    candidates = __itembag_merge__(map(lambda e: e.assemblecandidates(options), pointerdb))
    assemblings = filter(lambda i: candidates[i]>=options['threshold'], candidates)
    for assembling in assemblings:
        pattern = u_pattern.copy().assemble(assembling)
        __prefixspan__(pointerdb, pattern, options, freqpatterns)
                
    #Append - Get append candidates
    candidates = __itembag_merge__(map(lambda e: e.appendcandidates(options), pointerdb))
    appendings = filter(lambda i: candidates[i]>=options['threshold'], candidates)
    for appending in appendings:
        pattern = u_pattern.copy().append(appending)
        __prefixspan__(pointerdb, pattern, options, freqpatterns)
                
    #Return
    return

def prefixspan(u_db, u_options):
    """Prefixspan entry call, takes a database in the null separator format and a dictionary of options and returns frequent patterns and their frequency."""
    p_db, z2i, ibag = __parse_db__(u_db)
    options = __parse_options__(u_options)
    candidates = __ffi__(options['threshold'], ibag)
    db = map(lambda seq: map(lambda iset: filter(lambda x: x in candidates, iset), seq), p_db)
    pointerdb = [options['DBPointer'](z_id, db) for z_id in range(len(db))]
    candidates = list(map(lambda x: options['Pattern']().assemble(x), candidates))
    freqpatterns = []
    for atomicseq in candidates:
            __prefixspan__(pointerdb, atomicseq, options, freqpatterns)
    if 'logic' in options:
        freqpatterns = list(filter(lambda x: options['logic'](x[0]) and options['minSize']<=len(x[0]) and options['minSseq']<=x[0].size(), freqpatterns))
    return freqpatterns
    
