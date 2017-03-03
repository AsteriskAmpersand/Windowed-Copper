import orderedset as oset
import copy as copymodule

class Pattern(object):
    def __init__(self):
        self.__tail__ = []
        self.__head__ = set()#Used to be Oset
        self.__last__ = -1
        return
    
    def copy(self):
        clone = Pattern()
        clone.__tail__ = copymodule.deepcopy(self.__tail__)
        clone.__head__ = copymodule.deepcopy(self.__head__)
        clone.__last__ = self.__last__
        return clone        
        
    def assemble(self, item):
        assert item > self.__last__
        new = self.copy()
        new.__head__.add(item)
        new.__last__ = item
        return new

    def appended(self):
        return len(self.__head__) == 1

    def append(self, item):
        new = self.copy()
        if new.__head__:
            new.__tail__.append(new.__head__)
        new.__head__ = set([item])#Used to be Oset
        new.__last__ = item
        return new

    def last(self):
        assert self.__last__ != -1
        return self.__last__

    def contained(self, itemset):
        return all((item in itemset for item in self.__head__))
            
    def __len__(self):
        return len(self.__tail__) + bool(self.__head__)

    def size(self):
        return len(self.__head__)

    def __str__(self):
        string = ''
        for iset in self.__tail__+[self.__head__]:
            string+='<'
            buffr = ''
            for item in iset:
                buffr+=str(item)+', '
            if buffr:
                string+=buffr[:-2]+'>'
            else:
                string+='>'
        return string

    def __repr__(self):
        return str(self)