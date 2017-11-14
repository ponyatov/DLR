	def lexer(self,src):
		# token types
		tokens = ['COMMAND','REGISTER']
		# regexp/action rules
		def t_REGISTER(t):
			r'R[0-9]+'
			t.value = int(t.value[1:])
			return t