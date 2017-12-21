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
		# push return address (Ip points to call parameter)
		self.R.append(self.Ip+1)
		self.Ip = self.program[self.Ip]			# jmp
		assert type(self.Ip) == int				# addr must be integer
		assert self.Ip < len(self.program)		# check range
	def ret(self):
		assert self.R							# check non-empty
		self.Ip = self.R.pop()					# return to marked address
	
	def jmp(self):
		self.Ip = self.program[self.Ip]			# get addr from jmp parameter
		assert self.Ip < len(self.program)		# check range
	def qjmp(self):
		assert self.D
		if not self.D.pop(): # ( flag -- ) 
			self.jmp()
		else:
			self.Ip += 1	# skip ?jmp parameter
	def execute(self):
		self.R.append(self.Ip)					# push ret addr
		assert self.D ; self.Ip = self.D.pop()	# load jmp addr from stack
		assert type(self.Ip) == int				# addr must be integer
		assert self.Ip < len(self.program)		# check range
	def abort(self):
		print '\n\nD:%s\nR:%s\n' % (self.D,self.R)
# 		self.dump()
		raise BaseException('ABORT')

	def ld(self):
		' load register '
		assert self.Ip +2 < len(self.program)	# check Ip
		index = self.program[self.Ip]           # get register number
		assert index < len(self.R)              # check index
		self.Ip += 1                            # skip first command parameter
		data = self.program[self.Ip]            # load data to be loaded
		self.Ip += 1                            # skip second command parameter
		self.R[index] = data					# load register
		
	def fetch(self):
		assert self.D ; addr = self.D.pop()
		assert addr < len(self.program)
		self.D.append(self.program[addr])
	def store(self):
		pass
	def lit(self):
		self.D.append(self.program[self.Ip])
		self.Ip += 1

	# return known label for given address
	def log_label(self,addr): return ''
	# dump command from given addr
	def log_command(self,addr):
		A = addr
		# current command
		command = self.program[A]
		# check if we have known labels
		L = self.log_label(A)
		if L: print '\n%s:' % L, # print on separate line
		# print main command log text
		print '\n\t%.4X' % A , command,
		# process commands with parameters
		if command in [ VM.jmp, VM.qjmp, VM.call, VM.lit]:
			# target address
			T = self.program[A+1]
			# print target addr with known label
			print '%.4X'%T,self.log_label(T),
			A += 1
		return A+1	# return next command address
	# log extra state (in interpreter trace)
	def log_state(self):
		print self.Rg,
		
	def interpreter(self):
		self._bye = False		   				# stop flag
		while not self._bye:
			assert self.Ip < len(self.program)
			command = self.program[self.Ip]				# FETCH command
			self.log_command(self.Ip)		# log command
			self.log_state()				# log state
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
	def p_NOP(self,p):
		' command : NOP '
		self.program.append(self.nop)
	def p_BYE(self,p):
		' command : BYE '
		self.program.append(self.bye)
	def p_Rload(self,p):
		' command : REGISTER EQ constant'
		self.program.append(self.ld)	# compile ld command opcode
		self.program.append(p[1])		# compile register number at pos $1
		self.program.append(p[3])		# compile constant
	def p_STRING(self,p):
		' constant : STRING '
		p[0] = p[1]
	# required parser error callback must be method
	def p_error(self,p): raise SyntaxError('parser: %s' % p)
	
	def init_code(self):
		# set instruction pointer entry point
		self.Ip = 0							
		# clean up program memory	
		self.program = []
	def compiler(self,src):
		# ===== init code section =====
		self.init_code()

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
 		# loop over self.program
 		addr = 0;
 		# loop over program 
 		while addr < len(self.program):
 			# addr: command <extra>
 			addr = self.log_command(addr)
   		print ; print '-'*55
  			
	def __init__(self, P=''):
		self.compiler(P)						# run parser/compiler
		self.dump()								# dump compiled program
		self.interpreter()		  				# run interpreter

class FORTH(VM):
	
	Rg = ld = None	# throw out registers
	
	PAD = list('hello world ')
	def word(self):
		# result string
		S = ''
		# spaces
		BL = ' \t\r\n'
		# skip leading spaces
		try:
			while True:
				# pop first char from input stream
				C = self.PAD.pop(0)
				# break loop on non-space char
				if C not in BL: break
			# save first found non-BL char
			S += C
			# collect until BL char
			while True:
				C = self.PAD.pop(0)
				if C in BL: break
				S += C
		except IndexError: sys.exit(0)
		# push collected string
		self.D.append(S)
	
	def find(self):
		# pop word name from data stack
		S = self.D.pop()
		try:
			# push cfa of found word
			self.D.append(self.voc[S])
			# push FOUND flag
			self.D.append(True)
		except KeyError:
			# on error push word name
			self.D.append(S)
			# push NOT FOUND
			self.D.append(False)

	# command lookup table
	cmd = { 'nop':VM.nop , 'bye':VM.bye ,
			'jmp':VM.jmp, '?jmp':VM.qjmp, 
			'call':VM.call, 'ret':VM.ret,
			'execute':VM.execute, 'abort':VM.abort,
			'word':word, 'find':find,
			'@':VM.fetch,'!':VM.store,'lit':VM.lit }
	# vocabulary of all defined words
	voc = {}
	# reversed vocabulary {addr:name} for fast label lookup
	revoc = {}
	
	def log_state(self):
		print 'D:%s'%self.D,'R:%s'%self.R,
	def log_label(self,addr):
		try: return self.revoc[addr]
		except KeyError: return ''
		
	def dump(self):
		print self.voc
		VM.dump(self)
	
	def init_code(self):
		VM.init_code(self)
		self.program.append(VM.call)	# call ...
		self.program.append(0)			# _entry = 1
		self.program.append(VM.bye)		# bye

	t_ignore_COMMENT = r'\#.*|\\.*|\(.*?\)'				# comment
	tokens = ['ID','CMD','VOC',
				'COLON','SEMICOLON','BEGIN','AGAIN',
				'IF','ELSE','ENDIF',
				'NUM','VAR','FETCH','STORE','TRUE','FALSE']
	t_NOP = p_NOP = None
 	t_BYE = p_BYE = None
 	t_REGISTER = p_Rload = p_STRING = None
 	# lexemes regexp overrides
 	t_COLON = ':' ; t_SEMICOLON = ';'
 	def t_BEGIN(self,t):
 		r'begin'
 		return t 
 	def t_AGAIN(self,t):
 		r'again'
 		return t
 	def t_IF(self,t):
 		r'if'
 		return t
 	def t_ELSE(self,t):
 		r'else'
 		return t
 	def t_ENDIF(self,t):
 		r'endif'
 		return t
 	def t_VAR(self,t):
 		r'var'
 		return t
	def t_FETCH(self,t):
		r'\@'
		return t
	def t_STORE(self,t):
		r'\!'
		return t
 	def t_TRUE(self,t):
 		r'true'
 		return t
 	def t_FALSE(self,t):
 		r'false'
 		return t
 	def t_NUM(self,t):
  		r'0x[0-9A-Fa-f]+|0b[01]+|[\+\-]?[0-9]+(\.[0-9]*)?([eE][\+\-]?[0-9]+)?'
  		if t.value[:2] == '0x':
  			t.value = int(t.value[2:],0x10) # hex
  		elif t.value[:2] == '0b':
  			t.value = int(t.value[2:],0x02) # bin
  		else:
  			t.value = float(t.value)
 		return t
 	def t_ID(self,t): # this rule must be last rule
 		r'[a-zA-Z0-9_]+'
 		# first lookup in vocabulary
 		if t.value in self.voc: t.type='VOC'
 		# then check is it command name
 		if t.value in self.cmd: t.type='CMD'
 		return t 
 	# grammar override
 	def p_BEGIN(self,p):
		' command : BEGIN '
		# mark Ip pushing in return stack
		self.R.append(len(self.program))
 	def p_AGAIN(self,p):
		' command : AGAIN '
		# jmp opcode
		self.program.append(self.cmd['jmp'])
		# jmp parameter: pop marked Ip
		self.program.append(self.R.pop())
	def p_IF(self,p):
		' command : IF '
		self.program.append(self.cmd['?jmp'])	# opcode
		self.R.append(len(self.program))		# mark
		self.program.append(-1)					# fake addr
	def p_ELSE(self,p):
		' command : ELSE '
		assert self.R ; A = self.R.pop()		# pop if jmp
		self.program.append(self.cmd['jmp'])	# jmp endif
		self.R.append(len(self.program))		# mark
		self.program.append(-1)					# fake addr
		self.program[A] = len(self.program)		# backpatch if
	def p_ENDIF(self,p):
		' command : ENDIF '
		assert self.R ; A = self.R.pop()		# resolve
		self.program[A] = len(self.program)		# backpatch
# 		self.program.append(self.cmd['nop'])	# show endif pos
  	def p_ID(self,p):
		' command : ID '
#		raise BaseException(p[1])
 	def p_CMD(self,p):
 		' command : CMD '
 		# compile command using cmd{} lookup table
 		self.program.append(self.cmd[p[1]])
 	def p_VOC(self,p):
		' command : VOC '
		self.program.append(VM.call);		# opcode
		self.program.append(self.voc[p[1]])	# cfa
  	def p_COLON(self,p):
  		' command : COLON ID'
  		# store current compilation pointer into voc
		# reset _entry to current cfa
  		self.program[1] = self.voc[p[2]] = len(self.program)
  		# add reversed pair {addr:label}
  		self.revoc[len(self.program)] = p[2]
 	def p_SEMICOLON(self,p):
 		' command : SEMICOLON '
 		self.program.append(self.cmd['ret'])
 	def p_VAR(self,p):
 		' command : init VAR ID '
 		addr = len(self.program)
 		self.voc[p[3]] = addr ; self.revoc[addr] = p[3]
 		self.program.append(self.cmd['lit'])	 # lit ...
 		self.program.append(len(self.program)+2) # PFA
 		self.program.append(self.cmd['ret'])
 		self.program.append(p[1]) # compile PFA with init value
	def p_FETCH(self,p):
		' command : FETCH '
		self.program.append(self.cmd['@'])
	def p_STORE(self,p):
		' command : STORE '
		self.program.append(self.cmd['!'])
 	# var/const init value can be checked by syntax parser
 	def p_init_NUM(self,p):
 		' init : NUM '
 		p[0] = p[1]
 	def p_init_bool(self,p):
 		' init : bool '
 		p[0] = p[1]
 	def p_bool_true(self,p):
 		' bool : TRUE '
 		p[0] = True
 	def p_bool_false(self,p):
 		' bool : FALSE '
 		p[0] = False

if __name__ == '__main__':
	FORTH(r''' # use r' : we have escapes in string constants
: hello ;

false var STATE			\ interpret =0 / compile 

: INTERPRET				\ REPL interpreter /compiler loop
	begin
		\ get next word name from input stream
		word	( -- str:wordname )
		\ find word entry point
		find 	( addr:cfa true | str:wordname false )
		if ( addr:cfa )		 \ word found
			STATE @ ( bool ) \ compile =true / interpret =false
			if  
				abort
			else
				( addr:cfa ) execute \ call to addr from stack
			endif
		else ( str:wordname )
			\ dump state, stacks and restart
			abort
		endif		
	again			;		

	''')
