class VM:
	# program memory shared between VM instances
    program = []
    # constructor (re)loads program in P not empty  	
    def __init__(self, P=[]):
        self.R = [0,1,2,3,4,5,6,7]  # register pool
        if P: self.program = P		# load program
        ...    
