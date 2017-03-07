class TestF(object):
    def __init__ (self):
        print 'F'
        self.__f__=0

class TestS1(TestF):
    def __init__ (self):
        print 'S1'
        super(TestS1, self).__init__()
        self.__s1__=0
        
class TestS2(TestF):
    def __init__ (self):
        print 'S2'
        super(TestS2, self).__init__()
        self.__s2__=0

class TestD(TestS1, TestS2):
    def __init__ (self):
        print 'D'
        super(TestD, self).__init__()
        self.__d__=0
        print self.__d__
        print self.__s1__
        print self.__s2__
        print self.__f__
        
