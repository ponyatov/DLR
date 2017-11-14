	def lexer(self,src):
		# token types
		tokens = ['COMMAND']		
		# regexp/action rules
		def t_COMMAND(t):
			r'[a-z]+'
			return t
		# required lexer error callback
		def t_error(t): raise SyntaxError('lexer: %s' % t)
		# create ply.lex object
		lexer = lex.lex()				
		# feed source code
		lexer.input(src)				
		# get next token						 
		while True: print lexer.token()	
