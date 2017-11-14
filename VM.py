import sys

import ply.lex  as lex
import ply.yacc as yacc

class VM:
	D = []										# shared data stack
	R = []										# CALL/RET return stack
	
	R = [0,1,2,3,4,5,6,7]						# single register pool
	
    # command set
	def nop(self): pass             # do nothing
	def bye(self): self._bye=True   # stop singe VM only
	
	def ld(self):
		' load register '
		assert self.Ip +2 < len(self.program)	# check Ip
		index = self.program[self.Ip]           # get register number
		assert index < len(self.R)              # check index
		self.Ip += 1                            # skip first command parameter
		data = self.program[self.Ip]            # load data to be loaded
		self.Ip += 1                            # skip second command parameter
		self.R[index] = data					# load register

	def interpreter(self):
		self._bye = False		   				# stop flag
		while not self._bye:
			assert self.Ip < len(self.program)
			command = self.program[self.Ip]				# FETCH command
			print '%.4X' % self.Ip , command, self.R
			self.Ip += 1								# to next command
			command()									# DECODE/EXECUTE
			
	def compiler(self,src):
		self.Ip = 0								# set instruction pointer
		self.program = [ self.nop, self.bye ]	# (we don't have parser now)
		self.lexer(src)
		
	def lexer(self,src):
		# extra lexer states
		states = (('string','exclusive'),)
		# token types
		tokens = ['COMMAND','REGISTER','EQ','STRING']
		# regexp/action rules (ANY)
		def t_ANY_newline(t):					# special rule for EOL
			r'\n'
			t.lexer.lineno += 1					# increment line counter
			# do not return token, it will be ignored by parser
		# required lexer error callback
		def t_ANY_error(t): raise SyntaxError('lexer: %s' % t)
		# regexp/action rules (STRING)
		t_string_ignore = '' 				# don't ignore anything
		def t_string_end(t):
			r'\''
			t.lexer.pop_state()				# return to INITIAL
			t.type = 'STRING'				# overryde token type
			t.value = t.lexer.LexString 	# accumulator to value
			return t 						# return resulting string token
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
			r'.'
			t.lexer.LexString += t.value	# accumulate
		# regexp/action rules (INITIAL)
		def t_begin_string(t):
			r'\''
			t.lexer.push_state('string')
			t.lexer.LexString = ''			# initialize accumulator
		t_ignore = ' \t\r'					# drop spaces (no EOL)
		def t_COMMAND(t):
			r'[a-z]+'
			return t
		def t_REGISTER(t):
			r'R[0-9]+'
			t.value = int(t.value[1:])
			return t
		t_EQ = r'='
		# create ply.lex object
		lexer = lex.lex()				
		# feed source code
		lexer.input(src)				
		# get next token						 
		while True:
			next_token = lexer.token()
			if not next_token: break # on None
			print next_token 	
	
	def __init__(self, P=''):
		self.compiler(P)						# run parser/compiler
		self.interpreter()		  				# run interpreter

if __name__ == '__main__':
	VM(r'''
        R1 = 'R\t[1]'
        nop
        bye
	''')