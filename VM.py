# Dynamic FORTH/VM

import Queue

from SYM import *

# log = Queue.Queue() # logging

PAD = String('pad') # active wordpad text (will be parsed/executed)

PAD_Q = Queue.Queue()
def PAD_runner():
    while True:
        PAD.val = PAD_Q.get()
        print PAD.dump() ; print
        Interpreter()
        PAD_Q.task_done()
        
D   = Stack('data') # data stack
W   = Map('words')  # vocabulary (words)

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
        print 'ERROR:<%s>\n'%t
        global stop ; stop=True
        t.lexer.skip(len(t.lexer.lexdata)-t.lexer.lexpos)
    # feed lexer
    lexer = lex.lex() ; lexer.input(PAD.val)
    # FORTH is very simple language , use only lexer
    while not stop:
        token = lexer.token()
        if not token: break
        log.put('<%s>\n'%token)
