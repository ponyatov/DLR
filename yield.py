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

def parent(Person,Parent):
	for i in unify(Person,'Chelsea'):
		for j in unify(Parent,'Hillary'): yield
	for i in unify(Person,'Chelsea'):
		for j in unify(Parent,'Bill'): yield

def uncle(Person,Uncle):
	Parent = var()
	for i in parent(Person,Parent):
		for j in brother(Parent,Uncle): yield

def square(Width,Height): # square rectangle
	for i in unify(Width,Height): yield

for i in square(11,11):	# check 11 x 11
	print '11 x 11 is square'
W,H = var(),var()
for j in W << 22:
	for k in square(W,H):
		print W,H		# yields 22 x 22
W,H = var(),var()
for a in square(W,H):		# bind first
	for b in unify(W,33):		# unify with value
		print W,H

