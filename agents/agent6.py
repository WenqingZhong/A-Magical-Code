import itertools
import numpy as np
import string

#HYPERPARAMETERS

#first SAFE_CARDS amount of cards, we do not care about
#eg. we dont care about cards 0,1,2, ...., SAFE_CARDS-1
CARDS_FOR_ARITHMETIC_CODING = 20
ARITH_ACCURACY = 9

class Agent:
    def __init__(self):

        self.values = " "+string.ascii_lowercase

        #index of permutations
        #self.perm_idx = list(itertools.permutations(list(range(52-CARDS_FOR_ARITHMETIC_CODING, 52))))

    def encode(self, message):

        min_bound = 0
        max_bound = 1

        for c in message:
            ranges = np.linspace(min_bound,max_bound,len(self.values)+1)
            
            r = self.values.index(c)
            min_bound = ranges[r]
            max_bound = ranges[r+1]
        
        #the float of the value
        val = (max_bound+min_bound)/2
        print(val)
        
        #convert decimal to binary
        val_as_int = int(str(val)[2:2+ARITH_ACCURACY])
        print(val_as_int)
        val_as_bin = str(bin(val_as_int))[2:]
        print(val_as_bin)

        return

    def decode(self, deck):
        
        return "NULL"