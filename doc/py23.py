		# regexp/action rules (STRING)
		def t_string_tab(t):
			r'\\t'
			t.lexer.LexString += '\t'
		def t_string_cr(t):
			r'\\r'
			t.lexer.LexString += '\r'
		def t_string_lf(t):
			r'\\n'
			t.lexer.LexString += '\n'
		def t_string_char(t):				# must be last rule