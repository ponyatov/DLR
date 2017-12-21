# http://yieldprolog.sourceforge.net/tutorial1.html

def person():
    yield "Chelsea"
    yield "Hillary"
    yield "Bill"

for p in person(): print p
