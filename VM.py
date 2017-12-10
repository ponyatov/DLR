import sys 

sys.path.insert(0,'./ply')	# use fixed PLY: https://github.com/ponyatov/ply.git
import ply.lex  as lex
import ply.yacc as yacc
ply_class_inherit = True	# enable patches for parser class inheritance

class VM:
	Rg = [0,1,2,3,4,5,6,7]						# registers  

	D = []										# shared data stack

    											# ==== command set ===
	def nop(self): pass             			# do nothing
	def bye(self): self._bye=True				# stop singe VM only
	
	R = []										# CALL/RET return stack
	def call(self):
		self.R.append(self.program[Ip+1])		# push return address
		Ip = self.program[Ip]					# jmp
	def ret(self):
		assert length(self.R)					# check non-empty
		Ip = self.R.pop()						# return to marked address
	
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
			print '%.4X' % self.Ip , command, self.Rg
			self.Ip += 1								# to next command
			command(self)								# DECODE/EXECUTE
			
	# ===== lexer code section =====
	t_ignore = ' \t\r'					# drop spaces (no EOL)
	t_ignore_COMMENT = r'\#.*'			# line comment
	# regexp/action rules (ANY state)
	def t_ANY_newline(self,t):				# special rule for EOL
		r'\n'
		t.lexer.lineno += 1					# increment line counter
		# do not return token, it will be ignored by parser
	# token types
	tokens = ['NOP','BYE','REGISTER','EQ','STRING']
	# required lexer error callback
	def t_ANY_error(self,t): raise SyntaxError('lexer: %s' % t)
	def t_NOP(self,t):
		r'nop'
		return t
	def t_BYE(self,t):
		r'bye'
		return t

	# ===== parser/compiler code section =====
	def p_program_epsilon(self,p):
		' program : '
	def p_program_recursive(self,p):
		' program : program command '
	def p_command_NOP(self,p):
		' command : NOP '
		self.program.append(self.nop)
	def p_command_BYE(self,p):
		' command : BYE '
		self.program.append(self.bye)
	def p_command_R_load(self,p):
		' command : REGISTER EQ constant'
		self.program.append(self.ld)	# compile ld command opcode
		self.program.append(p[1])		# compile register number at pos $1
		self.program.append(p[3])		# compile constant
	def p_constant_STRING(self,p):
		' constant : STRING '
		p[0] = p[1]
	# required parser error callback must be method
	def p_error(self,p): raise SyntaxError('parser: %s' % p)
	
	def compiler(self,src):
		
		# ===== init code section =====
		
		# set instruction pointer entry point
		self.Ip = 0							
		# clean up program memory	
		self.program = []

		# ===== lexer code section =====
				
		# extra lexer states
		states = (('string','exclusive'),)

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
			
		def t_REGISTER(t):
			r'R[0-9]+'
			t.value = int(t.value[1:])
			return t
		t_EQ = r'='

		# create lexer object
		# note: we point on object (instance!) with rules 
		self.lexer = lex.lex(object=self)
		# feed source code
		self.lexer.input(src)

		# ===== parser/compiler code section =====
		# create ply.yacc object, without extra files
		parser = yacc.yacc(debug=False,write_tables=None,\
			module=self) # here we must point on instance
		# parse source code using lexer
		parser.parse(src,self.lexer)

  	def dump(self):	
  		print
  		for i in range(len(self.program)):
  			print '%.4X: %s' % (i,self.program[i])
  		print
  			
	def __init__(self, P=''):
		self.compiler(P)						# run parser/compiler
		self.dump()								# dump compiled program
		self.interpreter()		  				# run interpreter

class FORTH(VM):
	# command lookup table
	cmd = { 'nop':VM.nop , 'bye':VM.bye , 'call':VM.call, 'ret':VM.ret}
	# vocabulary of all defined words
	voc = {}
	
	t_ignore_COMMENT = r'\#.*|\\.*|\(.*?\)'				# comment
	tokens = ['ID','CMD','VOC',
				'COLON','SEMICOLON','BEGIN','AGAIN']
	t_NOP = p_command_NOP = None
 	t_BYE = p_command_BYE = None
 	t_REGISTER = p_command_R_load = p_constant_STRING = None
 	# lexemes regexp overrides
 	t_COLON = ':' ; t_SEMICOLON = ';'
 	def t_BEGIN(self,t):
 		r'begin'
 		return t 
 	def t_AGAIN(self,t):
 		r'again'
 		return t
 	def t_ID(self,t): # this rule must be last rule
 		r'[a-zA-Z0-9_]+'
 		# first lookup in vocabulary
 		if t.value in self.voc: t.type='VOC'
 		# then check is it command name
 		if t.value in self.cmd: t.type='CMD'
 		return t 
 	# grammar override
 	def p_command_BEGIN(self,p):	' command : BEGIN '
 	def p_command_AGAIN(self,p):	' command : AGAIN '
 	def p_command_CMD(self,p):
 		' command : CMD '
 		# compile command using cmd{} lookup table
 		self.program.append(self.cmd[p[1]])
 	def p_command_VOC(self,p):		' command : VOC '
  	def p_command_COLON(self,p):
  		' command : COLON ID'
  		# store current compilation pointer into voc
  		self.voc[p[2]] = len(self.program)
  		print self.voc
 	def p_command_SEMICOLON(self,p):
 		' command : SEMICOLON '
 		self.program.append(self.cmd['ret'])
  	def p_command_ID(self,p):		' command : ID '

if __name__ == '__main__':
	FORTH(r''' # use r' : we have escapes in string constants
nop bye
 
\ test FORTH comment syntax for inherited parser
: NOOP ;
: INTERPRET		\ REPL interpreter loop
	NOOP
	begin
		word	\ ( -- str:wordname ) get next word name from input stream
		find	\ ( str:wordname -- addr:xt ) find word entry point
		execute	\ ( xt -- ) execute found xt (execution token)
	again
;
	
	''')
