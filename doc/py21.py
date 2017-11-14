		# regexp/action rules (INITIAL)
		def t_begin_string(t):
			r'\''
			t.lexer.push_state('string')
		# regexp/action rules (STRING)
		def t_string_end(t):
			r'\''
			t.lexer.pop_state() # return to INITIAL