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

W['DUP'] = Fn(D.dup)
W['DROP'] = Fn(D.drop)
W['SWAP'] = Fn(D.swap)

# parser/interpreter

import ply.lex  as lex
import ply.yacc as yacc

def Interpreter():
    stop = False # flag
    tokens = ['NUM','WORDNAME','DOT','QUEST','unknown','outofdata']
    t_ignore = ' \t\r'
    t_ignore_COMMENT = '\#.+'
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    def t_NUM(t):
        r'[\+\-]?[0-9]+(\.[0-9]*)?([eE][\+\-]?[0-9]+)?'
        D << Number(t.value)
        return t
    def t_DOT(t):
        r'\.'
        D.dropall()
    def t_QUEST(t):
        r'\?'
        log.put(D.dump()+'\n\n')
    def t_WORDNAME(t):
        r'[a-zA-Z0-9_]+'
        N = t.value.upper()
        try: W.attr[N].fn()
        except KeyError: t.type = 'unknown' ; t_error(t)
        except IndexError: t.type = 'outofdata' ; t_error(t)
        return t
    def t_error(t):
        E = '\n\nERROR:<%s>\n' % t ; log.put(E) ; print E
        global stop ; stop=True                             # stop interpreter
        lexer.skip(len(lexer.lexdata)-lexer.lexpos)         # drop end of PAD
    # feed lexer
    lexer = lex.lex() ; lexer.input(PAD.val)
    # FORTH is very simple language , use only lexer
    while not stop:
        token = lexer.token()
        if not token: break
        log.put('<%s>\n'%token)
