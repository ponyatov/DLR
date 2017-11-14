	def lexer(self,src):
		# get next token						 
		while True:
			next_token = lexer.token()
			if not next_token: break # on None
			print next_token