 #We are treating multiple study domains as a preprocessing consideration to compact out into simple integer domains
import orderedset as oset
from seqpattern import Pattern
from dbpointer import DBPointer

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
            iset = oset.OrderedSet()
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
    assert 'threshold' in options
    assert isinstance( options['threshold'], ( int, long ) )

    options['Pattern'] = Pattern
    options['DBPointer'] = DBPointer
    
    return options

def __ffi__(support, itembag):
    """Returns frequent items from the itembag given support and itembag"""
    return [i for i in itembag if itembag[i]>=support]

def __itembag_merge__(itembaglist):#MISSING CODE
    mergedbag = {}
    for bag in itembaglist:
        for item in bag:
            if item in mergedbag:
                mergedbag[item]+=1
            else:
                mergedbag[item]=1
    return mergedbag

def __prefixspan__(u_pointerdb, u_pattern, options, freqpatterns):
    freqpatterns.append(u_pattern)
    #Projection
    pointerdb = []
    for entry in (entry.project(u_pattern) for entry in u_pointerdb):   
        if entry:                                                       
            pointerdb.append(entry)                                         
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
    """"""
    p_db, z2i, ibag = __parse_db__(u_db)
    options = __parse_options__(u_options)
    candidates = __ffi__(options['threshold'], ibag)
    db = map(lambda seq: map(lambda iset: filter(lambda x: x in candidates, iset), seq), p_db)
    pointerdb = [options['DBPointer'](z_id, db) for z_id in range(len(db))]
    candidates = list(map(lambda x: options['Pattern']().assemble(x), candidates))
    freqpatterns = []
    for atomicseq in candidates:
            __prefixspan__(pointerdb, atomicseq, options, freqpatterns)
    return freqpatterns
    
