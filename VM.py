# Dynamic FORTH/VM

from SYM import *

PAD = String('pad') # active wordpad text (will be parsed/executed)
D   = Stack('data') # data stack
W   = Map('words')  # vocabulary (words)

R   = Stack('ret')  # return stack (call/ret)

