	def lexer(self,src):
		# regexp/action rules
		t_ignore = ' \t\r'		# drop spaces (no EOL)
		def t_newline(t):		# special rule for EOL
			r'\n'
			t.lexer.lineno += 1	# increment line counter
			# do not return token,
			# it will be ignored by parser