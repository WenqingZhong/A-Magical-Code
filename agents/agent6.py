import itertools
import string
from decimal import *
import math

#HYPERPARAMETERS

#first SAFE_CARDS amount of cards, we do not care about
#eg. we dont care about cards 0,1,2, ...., SAFE_CARDS-1
CARDS_FOR_ARITHMETIC_CODING = 26
PADDING_CARDS = 52 - CARDS_FOR_ARITHMETIC_CODING
ARITH_ACCURACY = 26

getcontext().prec = 50

class Agent:
    def __init__(self):

        self.values = " "+string.ascii_lowercase

        #index of permutations
        #self.perm_idx = list(itertools.permutations(list(range(52-CARDS_FOR_ARITHMETIC_CODING, 52))))

        #arithmetic coding based on these frequencies
        #https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
        self.arithmatic_freq = {
            "e": 11.1607,
            "a": 8.4966,
            "r": 7.5809,
            "i": 7.5448,
            "o": 7.1635,
            "t": 6.9509,
            "n": 6.6544,
            "s": 5.7351,
            "l": 5.4893,
            "c": 4.5388,
            "u": 3.6308,
            "d": 3.3844,
            "p": 3.1671,
            "m": 3.0129,
            "h": 3.0034,
            "g": 2.4705,
            "b": 2.0720,
            "f": 1.8121,
            "y": 1.7779,
            "w": 1.2899,
            "k": 1.1016,
            "v": 1.0074,
            "x": 0.2902,
            "z": 0.2722,
            "j": 0.1000,
            "q": 0.1000,
            " ": 0.0961,
            "$": 0.965
        }

        self.arith_boundaries = {}

        total = 0
        prev = 0
        for c in self.arithmatic_freq:
            total += self.arithmatic_freq[c]/100.0
            self.arith_boundaries[c] = (prev, total if total <= 1 else 1)
            prev = total
        #print(self.arith_boundaries)

    def get_arithmatic_code(self, message):

        min_bound = Decimal(0)
        max_bound = Decimal(1)

        for c in message+"$":
            small, big = self.arith_boundaries[c]

            r = Decimal(max_bound-min_bound)

            min_bound += Decimal(small)*r
            max_bound = min_bound + Decimal(big-small)*r
            #print((max_bound+min_bound)/2)

        val = (max_bound+min_bound)/2
        return val

    def get_word(self, decimal_value):
        result = ""
        while len(result) < 30:
            for c in self.arith_boundaries:
                min_bound = Decimal(self.arith_boundaries[c][0])
                max_bound = Decimal(self.arith_boundaries[c][1])

                if decimal_value > min_bound and decimal_value < max_bound:
                    if c == "$":
                        return result
                    result += c
                    #print(result)
                    decimal_value = Decimal((decimal_value-min_bound) / (max_bound-min_bound))
                elif decimal_value == min_bound or decimal_value == max_bound:
                    raise Exception("Error in Parsing Word")
        return result

    def cards_to_number(self, cards):
        num_cards = len(cards)

        if num_cards == 1:
            return 0

        ordered_cards = sorted(cards)
        permutations = math.factorial(num_cards)
        sub_list_size = permutations // num_cards
        sub_list_indx = sub_list_size * ordered_cards.index(cards[0])

        #print(int(sub_list_indx))
        return int(sub_list_indx) + int(self.cards_to_number(cards[1:]))

    def number_to_cards(self, number, current_deck):
        num_cards = len(current_deck)

        if num_cards == 1:
            return current_deck

        ordered_cards = sorted(current_deck)
        permutations = math.factorial(num_cards)
        sub_list_size = permutations // num_cards
        sub_list_indx = int(Decimal(number) / sub_list_size)
        sub_list_start = sub_list_indx * sub_list_size

        if sub_list_start >= permutations:
            raise Exception('Number too large to encode in cards.')

        first_card = ordered_cards[sub_list_indx]
        ordered_cards.remove(first_card)
        #print(int(sub_list_start))
        return [first_card, *self.number_to_cards(int(number - sub_list_start), ordered_cards)]

    def encode(self, message):

        val = Decimal(self.get_arithmatic_code(message))
        
        #convert decimal to binary
        val_as_int = int(str(val)[2:2+ARITH_ACCURACY])

        #encode to a card sequence
        padded_cards = list(range(0,PADDING_CARDS))
        arith_cards = list(range(PADDING_CARDS, 52))

        print(val_as_int)
        encoded_cards = self.number_to_cards(val_as_int, arith_cards)

        #add padded cards to the end
        #print(encoded_cards)
        return padded_cards+encoded_cards

    def decode(self, deck):
        
        #Get order of last 26
        encoded_cards = []
        for num in deck:
            if num >= PADDING_CARDS:
                encoded_cards.append(num)
        #print(encoded_cards)
        #find the decimal value from it
        val = int(self.cards_to_number(encoded_cards))
        print(val)
        val_as_Decimal = Decimal("0."+str(val))

        #TODO IDEAS:
        #first card is the whether the number of 1's is even or odd
        #check the rest of the deck to confirm the number
        #check the delimiter at the end

        return self.get_word(val_as_Decimal)

if __name__ == "__main__":
    agent = Agent()
    message = "metabolic proces"
    deck = agent.encode(message)
    print(agent.decode(deck))