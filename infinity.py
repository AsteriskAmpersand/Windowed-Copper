"""
Infinity class for not relying on os/sys depandant calls such as MAXINT

Author: Agustin Guevara-Cogorno
Contact Details: a.guevarac@up.edu.pe
Institution: Universidad del Pacifico|University of the Pacific
"""
class Infinity(object):
    def __init__(self):
        return
    def __eq__(self, other):
        return False
    def __gt__(self, other):
        return True
    def __ge__(self, other):
        return True
    def __le__(self, other):
        return False
    def __lt__(self, other):
        return False
