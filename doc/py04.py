class VM:
    def ld(self):
        ' load register '
        assert self.Ip+2 < len(self.program)	# check Ip
        # get register number
        index = self.program[self.Ip]
        # skip _first_ command parameter
        self.Ip += 1                 
        # load data to be loaded
        data = self.program[self.Ip] 
        # skip _second_ command parameter
        self.Ip += 1                 
        # load register
        self.R[index] = data         
    def interpreter(self):
        ...
            print '%.4X' % self.Ip , command, self.R

if __name__ == '__main__':
    VM([                    # every command need VM. prefix
        VM.ld, 1, 'R[1]',   # R[1] <- 'string'
        VM.nop, VM.bye
    ])
