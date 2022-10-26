import itertools

#HYPERPARAMETERS

#first SAFE_CARDS amount of cards, we do not care about
#eg. we dont care about cards 0,1,2, ...., SAFE_CARDS-1
SAFE_CARDS = 52-7

class Agent:
    def __init__(self):

        #key = bit string
        #value = message
        self.message_dict = {}

        #number of total messages so far
        self.message_count = 0

        #index of permutations
        self.perm_idx = list(itertools.permutations(list(range(SAFE_CARDS, 52))))

    def encode(self, message):
        key = self.perm_idx[self.message_count]
        self.message_dict[key] = message
        self.message_count += 1

        return list(range(SAFE_CARDS)) + list(key)

    def decode(self, deck):
        
        key_builder = []
        for num in deck:
            if num >= SAFE_CARDS:
                key_builder.append(num)
        
        key = tuple(key_builder)

        if key in self.message_dict:
            return self.message_dict[key]

        return "NULL"