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
W['?'] = Fn(lambda: log.put(D.dump()+'\n\n'))

W['DUP'] = Fn(D.dup)
W['DROP'] = Fn(D.drop)
W['SWAP'] = Fn(D.swap)
W['OVER'] = Fn(D.over)

COMPILE = False

# parser/interpreter

import ply.lex  as lex
import ply.yacc as yacc

def Interpreter():
    stop = False # flag
    tokens = ['NUM','WORDNAME']
#     tokens = ['NUM',,'DOT','QUEST','unknown','outofdata',
#               'COLON','SEMICOLON']
    t_ignore = ' \t\r'
    t_ignore_COMMENT = '\#.+'
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    def t_NUM(t):
        r'[0-9]+'
        t.value = Number(t.value) ; return t
    def t_WORDNAME(t):
        r'[0-9a-zA-Z_\.\?\:]+'
        return t
    def t_error(t):
        E = '\n\nERROR:<%s>\n' % t ; log.put(E) ; print E
        global stop ; stop=True                             # stop interpreter
        lexer.skip(len(lexer.lexdata)-lexer.lexpos)         # drop end of PAD
    # feed lexer
    lexer = lex.lex() ; lexer.input(PAD.val)
    # FORTH is very simple language , use only lexer
    while not stop:
        t = lexer.token()
        if not t: break
        log.put('<%s>\n'%t)
        if COMPILE:
            raise BaseException
        else:
            if t.type == 'NUM':
                D.push(t.value)
            else:
                try: W.attr[t.value.upper()].eval()
                except KeyError: t.type = 'unknown' ; t_error(t)
                except IndexError: t.type = 'outofdata' ; t_error(t)
