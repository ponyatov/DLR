# http://yieldprolog.sourceforge.net/tutorial1.html

class var:						# Prolog unifying variable
	def __init__(self):
		self.bound = False      # unbound variable
	def __lshift__(self,val):   # unify operator <<
		if not self.bound:		# 1) unassigned
			self.value = val	# assign var
			self.bound = True
			yield
			self.bound = False	# drop binding
		elif self.value == val:	# 2) assigned == val
			yield
	def __repr__(self):         # dump in string form
		if self.bound:
			return '<bound:%s>' % self.value
		else:
			return '<unbound>'

def getval(V):				# return value or unbound var
	if isinstance(V,var):
		if not V.bound: return V
		else: return V.value
	else: return V

def unify(arg1,arg2):			# general unification
	arg1value = getval(arg1)		# \ get values
	arg2value = getval(arg2)		# /
	if isinstance(arg1value,var):	# unbound arg1
		for i in arg1value << arg2value: yield
	if isinstance(arg2value,var):	# unbound arg2
		for j in arg2value << arg1value: yield
	else:							# args non var's
		if arg1value == arg2value: yield

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

V = var()
for i in brother('Hillary',V):
	print '%s has brother %s.' % ('Hillary',V.value)
A,B = var(),var()
for j in brother(A,B): print B,'is brother of',A

