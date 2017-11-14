class VM:
	
	def __init__(self, P=''):
		self.compiler(P)                  # run parser/compiler
		self.interpreter()                # run interpreter

	def interpreter(self):
		self._bye = False                 # stop flag
		while not self._bye:
			...
			command = self.program[self.Ip] # FETCH command
			...
			self.Ip += 1                    # to next command
			command()                       # DECODE/EXECUTE

	def compiler(self,src):
		# set instruction pointer
		# (we will change it moving entry point)
		self.Ip = 0							
		# (we don't have parser now)	
		self.program = [ self.nop, self.bye ]
