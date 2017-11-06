import sys

# command set
def nop(): pass         # do nothing
def bye(): sys.exit(0)  # stop system

# we use Python parser and container
program = [ nop, bye ]

# interpreter
def interpreter():
    Ip=0
    while True:
        assert Ip < len(program)
        print '%.4X' % Ip, program[Ip] ; program[Ip]()
        Ip += 1

if __name__ == '__main__':
    interpreter()
