	def lexer(self,src):
		# extra lexer states
		states = (('string','exclusive'),) # don't forget comma