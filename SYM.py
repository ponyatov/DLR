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

# # print Object('+') .set('doc',Object('attribite')) \
# # 		<< Object(1) << Object(2.3) 
#  
# def test_Object():
#     assert re.match(r'obj #[0-9a-f]+', str(Object()))
     
class Primitive(Object): tag = 'prim'

# def test_Primitive():
#     assert re.match(r'prim: #[0-9a-f]+',str(Primitive()))
#     
# class Symbol(Primitive):
#     tag = 'sym'
# 
# def test_Symbol():
#     assert re.match(r'sym:xxx #[0-9a-f]+',str(Symbol('xxx')))
# 
# class Number(Primitive):
#     tag = 'num'
#     def __init__(self, V): Primitive.__init__(self,float(V))
# 
# def test_Number():
#     assert re.match(r'num:1.2 #[0-9a-f]+',str(Number('1.2')))
# 
# ###
# 
# # print Number('1.2')
# 
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
 
class Map(Collection): tag = 'map'

class OrderedCollection(Collection): tag ='ord'

class Stack(OrderedCollection): tag = 'stack'

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
        if len(N)>10: name = N[:10]+'...'
        return ' '*(10-len(name))+name
    def dump(self,depth=0):
        S = self.pad(depth) + self.head()
        for i in os.listdir(self.val):
            if not re.match(self.filter,i):
                S += self.pad(depth+1) + self.fname(i)
                if os.path.isdir(i): S += '/'
                else: S += '\t'+self.sz2h(os.stat(i)[6])
        return S

