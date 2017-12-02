import ply.lex  as lex
import ply.yacc as yacc

class VM:
	tokens = ['WORD']
	t_ignore = ' \t\r\n'
	def t_WORD(self,t):
		r'[a-z]+'
		print t
	def t_error(self,t): raise SyntaxError(t)
	def __init__(self,src=''):
		self.lexer = lex.lex(module=self)
		self.lexer.input(src)
		while self.lexer.token(): pass

class FORTH(VM):
	t_ignore = ' \t\r'
#	def t_newline(t):
#		r'\n'
#		t.lexer.line += 1

FORTH('''
	hello
		world
''')

