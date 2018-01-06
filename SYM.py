import re # for tests
def test_hello(): pass # use pytest

class Object:
    tag = 'obj'
    def __repr__(self): return '%s #%x'%(self.tag,id(self))
    
def test_Object():
    assert re.match(r'obj #[0-9a-f]+', str(Object()))
    
class Primitive(Object):
    tag = 'prim'
    def __init__(self): self.val = ''
    def __repr__(self): return '%s:%s #%x' % (self.tag, self.val, id(self))

def test_Primitive():
    assert re.match(r'prim: #[0-9a-f]+',str(Primitive()))
    
class Symbol(Primitive):
    tag = 'sym'
    def __init__(self, V): self.val = V

def test_Symbol():
    assert re.match(r'sym:xxx #[0-9a-f]+',str(Symbol('xxx')))

class Number(Primitive):
    tag = 'num'
    def __init__(self, V): self.val = float(V)

def test_Number():
    assert re.match(r'num:1.2 #[0-9a-f]+',str(Number('1.2')))

###

class Integer(Number):
	tag = 'int'
	def __init__(self,V): self.val = int(V)

print Integer('123')

class Hex(Integer):
	tag = 'hex'
	def __init__(self,V): self.val = int(V,0x10)
	def __repr__(self): return '%s:0x%X #%x' % (self.tag, self.val, id(self))

print Hex('0xFF')

class Binary(Integer):
	tag = 'bin'
	def __init__(self,V): self.val = int(V,0x02)
	def __repr__(self): return '%s:%s #%x' % (self.tag, "{0:b}".format(self.val), id(self))

print Binary('1111')

class Active(Object): tag = 'act'

class Operator(Active):
	tag = 'op'

print Operator('+')

