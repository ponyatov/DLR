import sys

class VM:
    R = [0,1,2,3,4,5,6,7]    # registers shared between VM instances
    # command set
    def nop(self): pass             # do nothing
    def bye(self): self._bye=True   # stop singe VM only

    def ld(self):
        ' load register '
        index = self.program[self.Ip]   # get register number
        self.Ip += 1                    # skip first command parameter
        data = self.program[self.Ip]    # load data to be loaded
        self.Ip += 1                    # skip second command parameter
        self.R[index] = data            # load register
         
    def interpreter(self):
        while not self._bye:
            assert self.Ip < len(self.program)
            command = self.program[self.Ip]
            print '%.4X' % self.Ip , command, self.R
            self.Ip += 1
            command(self)
    def __init__(self, P=[]):
        self.program = P        # load program
        self.Ip = 0             # set instruction pointer
        self._bye = False       # stop interpreter flag
        self.interpreter()      # run interpreter

if __name__ == '__main__':
    VM([                      # every command need VM. prefix
        VM.ld, 1, 'R[1]',
        VM.nop, VM.bye
    ])
