# http://yieldprolog.sourceforge.net/tutorial1.html

class Pvar: pass    # empty container class

def person(V):
    V.value = 'Chelsea' ; yield
    V.value = 'Hillary' ; yield
    V.value = 'Bill' ; yield

var = Pvar()
for p in person(var): print var.value
