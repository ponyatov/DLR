# http://yieldprolog.sourceforge.net/tutorial1.html

class Pvar:						# Prolog unifying variable
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

def person(V):
	for i in V << 'Chelsea'	: yield
	for i in V << 'Hillary'	: yield
	for i in V << 'Bill'	: yield

var = Pvar() ; print var
#for p in person(var): print var
for i in var << 'Hillary':
	for j in person(var):
		print var
for i in var << 'Buddy':
	for j in person(var):
		print var

