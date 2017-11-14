	def lexer(self,src):
		# token types
		tokens = ['COMMAND','REGISTER','EQ']
		# regexp/action rules
		t_EQ = r'='
