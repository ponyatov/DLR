# Dynamic FORTH/VM

import Queue

from SYM import *

PAD = String('pad') # active wordpad text (will be parsed/executed)

PAD_Q = Queue.Queue()
def PAD_runner():
    while True:
        PAD.val = PAD_Q.get()
        print PAD
        PAD_Q.task_done()

D   = Stack('data') # data stack
W   = Map('words')  # vocabulary (words)

R   = Stack('ret')  # return stack (call/ret)

