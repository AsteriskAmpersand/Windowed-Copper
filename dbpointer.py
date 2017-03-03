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

            

    
