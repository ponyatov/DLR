# http://yieldprolog.sourceforge.net/tutorial1.html

class var:						# Prolog unifying variable
	def __init__(self,name):
		self.bound = False      # unbound variable
		self.name = name
	def __lshift__(self,val):   # unify operator <<
		if not self.bound:		# 1) unassigned
			self.value = getval(val) # get var
			if self.value == self: yield # can be itself
			else:
				self.bound = True	# bound
				yield
				self.bound = False	# drop binding
		else:
			for i in unify(self,val): yield
	def __repr__(self):         # dump in string form
		if self.bound:
			return '%s=%s' % (self.name,self.value)
		else:
			return '%s' % self.name
	def getval(self):
		if not self.bound:		# return unbound as is
			return self
		V = self.value				# else do loop until
		while isinstance(V, var):	# non-variable found
			if not V.bound: return V # or unbound var
 			V = V.value				# scan var chain
		return V		

def getval(V):				# return value or unbound var
	if isinstance(V,var): return V.getval()
	else: return V

def unify(arg1,arg2):			# general unification
	arg1value = getval(arg1)		# \ get values
	arg2value = getval(arg2)		# /
	A = B = False
	if isinstance(arg1value,var):	# arg1 is variable
		A = True
 		for i in arg1value << arg2value: yield
	if isinstance(arg2value,var):	# arg2 is variable
		B = True
 		for j in arg2value << arg1value: yield
	if not (A and B):				# args non var's
		if arg1value == arg2value: yield

def square(Width,Height): # square rectangle
	for i in unify(Width,Height): yield

W,H = var('W'),var('H')
for a in square(W,H):	print W,H
for a in square(W,H):			# bind first
   	for b in unify(W,33):		# unify with value
 		print W,H
 		
##############################################################################
def person(V):
	for i in unify(V,'Chelsea'): yield
	for i in unify(V,'Hillary'): yield
	for i in unify(V,'Bill'):    yield

def brother(Person,Brother):
	for i in unify(Person,'Hillary'):
		for j in unify(Brother,'Tony'): yield
		for j in unify(Brother,'Hugh'): yield
	for i in unify(Person,'Bill'):
		for j in unify(Brother,'Roger'): yield

def parent(Person,Parent):
	for i in unify(Person,'Chelsea'):
		for j in unify(Parent,'Hillary'): yield
	for i in unify(Person,'Chelsea'):
		for j in unify(Parent,'Bill'): yield

def uncle(Person,Uncle):
	Parent = var()
	for i in parent(Person,Parent):
		for j in brother(Parent,Uncle): yield
