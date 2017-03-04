#import copy as copymodule
import itertools

class DBPointer(object):
    def __init__(self, zid, db):
        self.__origin__ = db
        self.__entry__ = zid
        self.__positions__ = [-1]
        self.__last__ = -1 #replaceable by passing pattern to the candidate searchers

    def partialcopy(self):
        new = DBPointer(self.__entry__, self.__origin__)
        return new
        
    def project(self, pattern):
        result = self.partialcopy()
        result.__last__ = pattern.last()
        if pattern.appended():
            result.__positions__ = result.__positions__ = [index+self.__positions__[0]+1 for index, itemset in enumerate(self.__origin__[self.__entry__][self.__positions__[0]+1:]) if pattern.last() in itemset]
        else:
            result.__positions__ = list(filter(lambda pos: pattern.last() in self.__origin__[result.__entry__][pos]
                                                , self.__positions__))
        return result

    def appendcandidates(self, options):
        candidates = set()
        for itemset in self.__origin__[self.__entry__][self.__positions__[0]+1:]:
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
        return intervallist1
    if (intervallist2[0][0]<intervallist1[0][0])and(intervallist2[0][1]>intervallist1[-1][1]):
        return intervallist2       
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
            
    return result
    

class WindowGapPointer(DBPointer):
    def __init__(self, zid, db):
        DBPointer.__init__(self, zid, db)
        self.__progenitor__ = []
        self.__previous__ = []
        
    def partialcopy(self):
        new = WindowGapPointer(self.__entry__, self.__origin__)
        return new
    
    def project(self, pattern):
        result = DBPointer.project(self, pattern)
        if pattern.appended():
            if not self.__progenitor__:
                result.__progenitor__ = self.__positions__
            result.__previous__ = self.__positions__
        return result

    def appendcandidates(self, options):
        candidates = set()
        ranges = __intervaln__(__intervalu__(options['window'](self.__progenitor__, len(self.__origin__[self.__entry__]))),
                      __intervalu__(options['gap'](self.__previous__, len(self.__origin__[self.__entry__]))))
        ranges = itertools.chain.from_iterable((range(max(interval[0],self.__positions__[0]+1), min(interval[1],len(self.__origin__[self.__entry__]))) for interval in ranges))
        for itemset in ranges:
            for item in itemset:
                candidates.add(item)
        return candidates
        
class CopperPointer (DBPointer):
    def __init__(self, zid, db):
        DBPointer.__init__(self, zid, db)
        self.__pattern__ = None

    def partialcopy(self):
        new = CopperPointer(self.__entry__, self.__origin__)
        return new

    def project(self, pattern):
        result = DBPointer.project(self, pattern)
        result.__pattern__ = pattern
        return result
    
    def appendcandidates(self, options):
        candidates = []
        if self.__pattern__.size()>=options['minSseq'] and len(self.__pattern__)<=options['maxSize']:
            candidates = DBPointer.appendcandidates(self, options)
        return candidates
                 
    def assemblecandidates(self,options):
        candidates = []
        if self.__pattern__.size()<=options['maxSseq']:
            candidates = DBPointer.assemblecandidates(self, options)
        return candidates
