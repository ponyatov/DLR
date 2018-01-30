# Dynamic object model
 
import re # for tests
def test_hello(): pass # use pytest
 
class Object:
    tag = 'obj'					# bind object type
    def __init__(self, V=''):
        self.val = V			# object single value
        self.attr={}			# attributes {key:value}
        self.nest=[]			# nested elements (ordered list)
    # dump object
    def __repr__(self): return self.dump()
    def head(self): return '%s:%s #%x' % (self.tag, self.val, id(self))
    def pad(self, N): return '\n'+'\t'*N
    def dump(self,depth=0,prefix=''):
        # tabbed object header tag:value #id
        S = self.pad(depth) + prefix + self.head()
        # dump attributes if exists
        for i in self.attr: S += self.attr[i].dump(depth+1,'%s = '%i)
        # dump nested elements if exists
        for j in self.nest: S += j.dump(depth+1)
        # return resulting dump string
        return S
    # add to nest[]ed using << operator
    def __lshift__(self,o): self.nest.append(o) ; return self
    # set attribute value
    def set(self,key,val): self.attr[key]=val ; return self

def test_Object():
    assert re.match(r'obj: #[0-9a-f]+', Object().head())
     
class Primitive(Object): tag = 'prim'

def test_Primitive():
    assert re.match(r'prim: #[0-9a-f]+',Primitive().head())
     
class Symbol(Primitive):
    tag = 'sym'

def test_Symbol():
    assert re.match(r'sym:xxx #[0-9a-f]+',Symbol('xxx').head())
 
class Number(Primitive):
     tag = 'num'
     def __init__(self, V): Primitive.__init__(self,float(V))
 
def test_Number():
    assert re.match(r'num:1.2 #[0-9a-f]+',Number('1.2').head())

# class Integer(Number):
# 	tag = 'int'
# 	def __init__(self, V): Primitive.__init__(self,int(V))
# 
# # print Integer('123')
# 
# class Hex(Integer):
# 	tag = 'hex'
# 	def __init__(self,V): Primitive.__init__(self,int(V,0x10))
# 	def head(self): return '%s:0x%X #%x' % (self.tag, self.val, id(self))
# 
# # print Hex('0xFF')
# 
# class Binary(Integer):
# 	tag = 'bin'
# 	def __init__(self,V): Primitive.__init__(self,int(V,0x02))
# 	def head(self): return '%s:%s #%x' % (self.tag, "{0:b}".format(self.val), id(self))
# 
# # print Binary('1111')

class String(Primitive): tag = 'str'

# class Active(Object): tag = 'act'
# 
# class Operator(Active):
# 	tag = 'op'
# 
# # print \
# # 	Operator("+") \
# # 		<< Integer(1) \
# # 		<< Number('2.3') \
# # 	<< Operator('*') \
# # 		<< Symbol('X')

class Collection(Object): tag = 'coll'
 
class Map(Collection):
    tag = 'map'
    def __setitem__(self,K,V): self.attr[K] = V

class OrderedCollection(Collection):
    tag ='ord'
    def dropall(self): self.nest = []

class Stack(OrderedCollection):
    tag = 'stack'
    def dup(self): self.push(self.top())
    def top(self): return self.nest[-1]
    def push(self,o): self.nest.append(o)
    def drop(self): self.pop()
    def pop(self): return self.nest.pop()
    def swap(self):
        A = self.pop() ; B = self.pop()
        self.push(A) ; self.push(B)
    def over(self): self.nest.append(self.nest[-2])

# action

class Action(Object): tag = 'act'

class Fn(Action):
    tag = 'fn'
    def __init__(self,V):
        Action.__init__(self, V.__name__)
        self.fn = V
    def eval(self): self.fn()
        
class Code(Action):
    tag = 'code'

# #print Stack('data') << Integer(1) << Number(2.3)

import os

class IO(Object): tag = 'io'
 
class Dir(IO):
    tag = 'dir'
    filter = '^\..+|.+\~$'
    def __init__(self,V=os.getcwd()): IO.__init__(self,V)
    def sz2h(self,N):
        if N > 1024*1024: return '%sM'%(N/1024/1024)
        if N > 1024     : return '%sk'%(N/1024     )
        return '%s'%N
    def fname(self,N):
        name = N
        if len(N)>22: name = N[:10]+'...'
        return ' '*(22-len(name))+name
    def dump(self,depth=0):
        S = self.pad(depth) + self.head()
        for i in os.listdir(self.val):
            if not re.match(self.filter,i):
                S += self.pad(depth+1) + self.fname(i)
                if os.path.isdir(i): S += '/'
                else: S += '\t'+self.sz2h(os.stat(i)[6])
        return S

