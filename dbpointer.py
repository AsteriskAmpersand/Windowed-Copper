"""
Pointer to Database class for use with Prefixspan.
Different classes correspond to different functionality and capabilities.
DBPointer - Prefixspan, CopperPointer - COPPER,
GapCop - Combined Copper and Gap, WindowPointer - Window Features combined with all of the above

Author: Agustin Guevara-Cogorno
Contact Details: a.guevarac@up.edu.pe
Institution: Universidad del Pacifico|University of the Pacific
"""
import copy as copymodule
import itertools

class DBPointer(object):
    def __init__(self, zid, db):
        self.__origin__ = db
        self.__entry__ = zid
        self.__positions__ = [-1]
        self.__last__ = -1

    def partialcopy(self):
        new = self.__class__(self.__entry__, self.__origin__)
        return new
        
    def project(self, pattern, options):
        result = self.partialcopy()
        result.__last__ = pattern.last()
        if pattern.appended():
            result.__positions__ = [index+self.__positions__[0]+1
                                            #enumerate(self.__origin__[self.__entry__][self.__positions__[0]+1:])
                                            #=enumerate((self.__origin__[self.__entry__][i] for i in range(self.__positions__[0]+1, len(self.__origin__[self.__entry__]))))
                                            for index, itemset in enumerate((self.__origin__[self.__entry__][i] for i in range(self.__positions__[0]+1, len(self.__origin__[self.__entry__]))))
                                            if pattern.last() in itemset]
        else:
            result.__positions__ = list(filter(lambda pos: pattern.last() in self.__origin__[result.__entry__][pos]
                                                , self.__positions__))
        return result

    def appendcandidates(self, options):
        candidates = set()
                        #self.__origin__[self.__entry__][self.__positions__[0]+1:]
        for itemset in (self.__origin__[self.__entry__][i] for i in range(self.__positions__[0]+1, len(self.__origin__[self.__entry__]))):
            for item in itemset:
                candidates.add(item)
        return candidates
                
        
    def assemblecandidates(self,options):
        candidates = set()
        for pos in self.__positions__:
            for val in filter(lambda x: x > self.__last__, self.__origin__[self.__entry__][pos]):
                candidates.add(val)
        return candidates

    def __nonzero__(self):
        return bool(self.__positions__)

def __intervalu__(intervallist):
    """Clopen interval union using linesweep"""
    result = []
    for interval in intervallist:
        if not result:
            result.append([x for x in interval])
        else:
            if interval[0]<=result[-1][1]:
                result[-1][1]=max(result[-1][1],interval[1])
            else:
                result.append([x for x in interval])
    return result

class __IntervalPointer__(object):
    def __init__(self, ref):
        self.ref = ref
        self.pos = 0
        self.lim = len(ref)
    def __getitem__(self, arg):
        return self.ref[self.pos][arg]
    def peek(self,arg):
        return self.ref[self.pos+1][arg]
    def next(self):
        self.pos+=1
        return
    def check(self):
        return bool(self) and self.pos+1<self.lim
    def __nonzero__(self):
        return self.pos<self.lim

def __intervaln__(intervallist1, intervallist2):
    """Interval intersection between two list of disjoint clopen intervals using linesweep"""
    result = []
    if not(intervallist1 and intervallist2):
        return result
    if (intervallist1[0][0]<intervallist2[0][0])and(intervallist1[0][1]>intervallist2[-1][1]):
        return intervallist2
    if (intervallist2[0][0]<intervallist1[0][0])and(intervallist2[0][1]>intervallist1[-1][1]):
        return intervallist1       
    j = 0 if intervallist1[0][0] < intervallist2 [0][0] else 1
    q = (j+1)%2
    i=(__IntervalPointer__(intervallist1), __IntervalPointer__(intervallist2))
    while i[0] and i[1]:
        while i[j].check() and i[j].peek(0)<i[q][0]:
            i[j].next()
        if i[q][0]>=i[j][1]:
            i[j].next()
            j,q=q,j
        else:
            result.append([max(i[j][0],i[q][0]),min(i[j][1],i[q][1])])
            if i[j][1]<i[q][1]:
                j,q = q,j
            i[q].next()
    if result:
        assert result[0][0]>=intervallist1[0][0]
        assert result[0][0]>=intervallist2[0][0]
    return result
    

#WRONG requires rewrite of window. Currently consider [a] [b] [a c] [b d] [c] win =2
#Window instead should make the DB a partition for each starting point and each time it does projection candidates
#when no window partition it's a single partition [[DB]]
#when window is present the algorithm changes... almost completely since one must keep track of the starting points per each repartitioning of each entry
# {[a] [b] [a c]} {[a c] [b d] [c]}
# and last locations pointings must also be an array of arrays of positions

class GapPointer(DBPointer):
    def __init__(self, zid, db):
        super(GapPointer, self).__init__(zid, db)
          
    def project(self, pattern, options):        
        if self.__last__ == -1:
            result = super(GapPointer, self).project(pattern, options)
            return result
        result = self.partialcopy()
        result.__last__ = pattern.last()
        if pattern.appended():
            ranges = __intervalu__(options['gap'](self.__positions__, len(self.__origin__[self.__entry__])))
            rangeiter = itertools.chain.from_iterable((range(interval[0], interval[1]) for interval in ranges))
            result.__positions__ = [index
                                        for index, itemset in ((pos, self.__origin__[self.__entry__][pos]) for pos in rangeiter)
                                        if pattern.last() in itemset]
        else:
            result.__positions__ = list(filter(lambda pos: pattern.last() in self.__origin__[result.__entry__][pos]
                                                , self.__positions__))
        return result

    def appendcandidates(self, options):
        candidates = set()
        ranges = __intervalu__(options['gap'](self.__positions__, len(self.__origin__[self.__entry__])))
        rangeiter = itertools.chain.from_iterable((range(interval[0], min(interval[1],len(self.__origin__[self.__entry__]))) for interval in ranges))
        for pos in rangeiter:
            for item in self.__origin__[self.__entry__][pos]:
                candidates.add(item)
        return candidates
        
class CopperPointer (DBPointer):
    def __init__(self, zid, db):
        super(CopperPointer, self).__init__(zid, db)
        self.__pattern__ = None

    def project(self, pattern, options):
        result = super(CopperPointer, self).project(pattern, options)
        result.__pattern__ = pattern
        return result
    
    def appendcandidates(self, options):
        candidates = []
        if self.__pattern__.size()>=options['minSseq'] and len(self.__pattern__)<options['maxSize']:
            candidates = super(CopperPointer, self).appendcandidates(options)
        return candidates
                 
    def assemblecandidates(self,options):
        candidates = []
        if self.__pattern__.size()<options['maxSseq']:
            candidates = super(CopperPointer, self).assemblecandidates(options)
        return candidates    

class GapCopPointer (CopperPointer, GapPointer):
    def __init__(self, zid, db):
        super(GapCopPointer, self).__init__(zid, db)

    def partialcopy(self):
        new = GapCopPointer(self.__entry__, self.__origin__)
        return new        

    def project(self, pattern, options):
        result = GapPointer.project(self, pattern, options)
        result.__pattern__ = pattern
        return result
    
    def appendcandidates(self, options):
        candidates = []
        if self.__pattern__.size()>=options['minSseq'] and len(self.__pattern__)<options['maxSize']:
            candidates = GapPointer.appendcandidates(self, options)
        return candidates
                 
    def assemblecandidates(self,options):
        candidates = []
        if self.__pattern__.size()<options['maxSseq']:
            candidates = GapPointer.assemblecandidates(self, options)
        return candidates          

class SegmentIterator(object):
    def __init__(self, source, start, end):
        self.__source__ = source
        self.__pos__ = start
        self.__end__ = min(end, len(source))
    def __iter__(self):
        return self
    def next(self):
        if self.__pos__ < self.__end__:
            n = self.__source__[self.__pos__]
            self.__pos__+=1
            return n
        else:
            raise StopIteration
    

class StaticListSegment(object):
    def __init__(self, source, start, end):
        self.__source__ = source
        self.__start__ = start
        self.__end__ = min(end, len(source))
        return
    def __getitem__(self, key):
        assert key < len(self)
        return self.__source__[key+self.__start__]
    def __iter__(self):
        return SegmentIterator(self.__source__, self.__start__, self.__end__)
    def __len__(self):
        return self.__end__ - self.__start__

    

class WindowPointer(object):
    def __init__(self, zid, db, pointerclass):
        self.__origin__ = db
        self.__entry__ = zid
        self.__pclass__ = pointerclass
        self.__partitioned__ = False
        return
        
    def __partialcopy__(self):
        new = WindowPointer(self.__entry__, self.__origin__, self.__pclass__)
        return new
    
    def project(self, pattern, options):
        result = self.__partialcopy__()
        if not self.__partitioned__:
            partition = []
            for ocurrence in (pos for pos, i in enumerate(self.__origin__[self.__entry__]) if pattern.last() in i):
                    partition.append(StaticListSegment(self.__origin__[self.__entry__], ocurrence, ocurrence+options['window']) )
                    if ocurrence+options['window']>=len(self.__origin__[self.__entry__]):
                        break                              
            self.__pointers__ = [self.__pclass__(z_id, partition) for z_id in range(len(partition))]
        result.__pointers__ = [w for w in (x.project(pattern, options) for x in self.__pointers__) if w]
        result.__partitioned__ = True
        return result

    def appendcandidates(self, options):
        assert self.__partitioned__
        candidates = reduce(lambda x,y: x|y, (p.appendcandidates(options) for p in self.__pointers__), set())
        return candidates
              
    def assemblecandidates(self,options):
        assert self.__partitioned__
        candidates = reduce(lambda x,y: x|y, (p.assemblecandidates(options) for p in self.__pointers__), set())
        return candidates

    def __nonzero__(self):
        assert self.__partitioned__
        return bool(self.__pointers__)
