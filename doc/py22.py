		# token types
		tokens = ['COMMAND','REGISTER','EQ','STRING']
		# regexp/action rules (INITIAL)
		def t_begin_string(t):
			r'\''
			t.lexer.push_state('string')
			t.lexer.LexString = '' # initialize accumulator
		# regexp/action rules (STRING)
		def t_string_char(t):
			r'.'
			t.lexer.LexString += t.value # accumulate
		def t_string_end(t):
			r'\''
			t.lexer.pop_state() # return to INITIAL
			t.type = 'STRING'					# overryde token type
			t.value = t.lexer.LexString # accumulator to value
			return t # return resulting string token