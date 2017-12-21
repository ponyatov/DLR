# http://yieldprolog.sourceforge.net/tutorial1.html

class Pvar:
    def __init__(self):
        self.bound = False      # unbound variable
    def __lshift__(self,val):   # assign operator <<
        self.bound = True
        self.value = val
    def __repr__(self):         # dump in string form
        if self.bound:
            return '<bound:%s>' % self.value
        else:
            return '<unbound>'

def person(V):
    V << 'Chelsea' ; yield
    V << 'Hillary' ; yield
    V << 'Bill'    ; yield

var = Pvar() ; print var
for p in person(var): print var
