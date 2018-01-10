# Dynamic FORTH/VM

import Queue

from SYM import *

log = Queue.Queue() # logging

PAD = String('pad') # active wordpad text (will be parsed/executed)

PAD_Q = Queue.Queue()
def PAD_runner():
    while True:
        PAD.val = PAD_Q.get()
        log.put(PAD.dump()+'\n')
        Interpreter()
        PAD_Q.task_done()
        
W   = Map('words')  # vocabulary (words)

D   = Stack('data') # data stack

R   = Stack('ret')  # return stack (call/ret)

def WORDS(): log.put(W.dump())
W['WORDS'] = Fn(WORDS)


# parser/interpreter

import ply.lex  as lex
import ply.yacc as yacc

def Interpreter():
    stop = False # flag
    tokens = ['WORDNAME','DOT','QUEST']
    t_ignore = ' \t\r'
    t_ignore_COMMENT = '\#.+'
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    def t_DOT(t):
        r'\.'
        D.dropall()
    def t_QUEST(t):
        r'\?'
        log.put(D.dump()+'\n\n')
    def t_WORDNAME(t):
        r'[a-zA-Z0-9_]+'
        return t
    def t_error(t):
        error(t,t.lexer)
    def error(msg,lexer):
        E = '\n\nERROR:<%s>\n' % msg ; log.put(E) ; print E
        global stop ; stop=True                             # stop interpreter
        lexer.skip(len(lexer.lexdata)-lexer.lexpos)         # drop end of PAD
    # feed lexer
    lexer = lex.lex() ; lexer.input(PAD.val)
    # FORTH is very simple language , use only lexer
    while not stop:
        token = lexer.token()
        if not token: break
        log.put('<%s>\n'%token)
        N = token.value.upper()
        try:
            W.attr[N].fn()
        except KeyError:
            error('unknown: %s' % token,lexer)
