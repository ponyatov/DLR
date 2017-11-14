		# regexp/action rules (ANY)
		# required lexer error callback
		def t_ANY_error(t): raise SyntaxError('lexer: %s' % t)
		# regexp/action rules (STRING)
		t_string_ignore = '' # don't ignore anything
