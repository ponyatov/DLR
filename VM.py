import sys

class VM:
	D = []										# shared data stack
	R = []										# CALL/RET return stack
	
	R = [0,1,2,3,4,5,6,7]						# single register pool
	
    # command set
	def nop(self): pass             # do nothing
	def bye(self): self._bye=True   # stop singe VM only
	
	def ld(self):
		' load register '
		assert self.Ip +2 < len(self.program)	# check Ip
		index = self.program[self.Ip]           # get register number
		assert index < len(self.R)              # check index
		self.Ip += 1                            # skip first command parameter
		data = self.program[self.Ip]            # load data to be loaded
		self.Ip += 1                            # skip second command parameter
		self.R[index] = data					# load register

	def interpreter(self):
		self._bye = False		   				# stop flag
		while not self._bye:
			assert self.Ip < len(self.program)
			command = self.program[self.Ip]				# FETCH command
			print '%.4X' % self.Ip , command, self.R
			self.Ip += 1								# to next command
			command()									# DECODE/EXECUTE
			
	def compiler(self,src):
		self.Ip = 0								# set instruction pointer
		self.program = [ self.nop, self.bye ]	# (we don't have parser now)
	
	def __init__(self, P=''):
		self.compiler(P)						# run parser/compiler
		self.interpreter()		  				# run interpreter

if __name__ == '__main__':
	VM('''
        R1 = 'R[1]'
        nop
        bye
	''')