import re # for tests
def test_hello(): pass # use pytest

class Object:
    tag = 'obj'
    def __repr__(self): return '%s #%x'%(self.tag,id(self))
    
def test_Object():
    assert re.match(r'obj #[0-9a-f]+', str(Object()))
    
class Primitive(Object):
    tag = 'prim'

def test_Primitive():
    assert re.match(r'prim #[0-9a-f]+',str(Primitive()))
    
class Symbol(Primitive):
    tag = 'sym'
    def __init__(self,V): self.val = V    
print Symbol('xxx')
