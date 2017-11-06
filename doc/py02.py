import sys

class VM:
    # command set
    def nop(self): pass             # do nothing
    def bye(self): self._bye=True   # stop single VM only
    # sequence interpreter
    def interpreter(self):
        while not self._bye:
            assert self.Ip < len(self.program)
            command = self.program[self.Ip]
            print '%.4X' % self.Ip , command
            self.Ip += 1
            command(self)
    # virtual machine constructor
    def __init__(self, P=[]):
        self.program = P        # load program
        self.Ip = 0             # set instruction pointer
        self._bye = False       # stop interpreter flag
        self.interpreter()      # run interpreter

if __name__ == '__main__':
    VM([ VM.nop, VM.bye ])  # every command need VM. prefix
