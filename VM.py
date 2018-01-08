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


# parser/interpreter

import ply.lex  as lex
import ply.yacc as yacc

def Interpreter():
    stop = False # flag
    tokens = ['WORDNAME']
    def t_WORDNAME(t):
        r'[a-zA-Z0-9_]+'
        return t
    def t_error(t):
        E = 'ERROR:<%s>\n'%t ; log.put(E) ; print E
        global stop ; stop=True                             # stop interpreter
        t.lexer.skip(len(t.lexer.lexdata)-t.lexer.lexpos)   # drop end of PAD
    # feed lexer
    lexer = lex.lex() ; lexer.input(PAD.val)
    # FORTH is very simple language , use only lexer
    while not stop:
        token = lexer.token()
        if not token: break
        log.put('<%s>\n'%token)
