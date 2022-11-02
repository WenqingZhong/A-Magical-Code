from cards import generate_deck
import numpy as np
from itertools import permutations
import math

class Agent:
    def __init__(self):
        self.huff_LtoB = {
            'a': '1111',
            'b': '100000',
            'c': '00000',
            'd': '11101',
            'e': '110',
            'f': '00011',
            'g': '100001',
            'h': '0111',
            'i': '0110',
            'j': '0001010111',
            'k': '0001011',
            'l': '11100',
            'm': '00001',
            'n': '1001',
            'o': '1011',
            'p': '01000',
            'q': '000101010',
            'r': '1010',
            's': '0101',
            't': '001',
            'u': '01001',
            'v': '000100',
            'w': '100011',
            'x': '00010100',
            'y': '100010',
            'z': '0001010110'
        }
        self.huff_BtoL = {}
        for l in self.huff_LtoB:
            binary = self.huff_LtoB[l]
            self.huff_BtoL[binary] = l

        self.zero_permu_map=self.get_permutation_map(4)

    def get_permutation_length(self,num):
        permutation_length=0
        for i in range(1, 53):
            num_permu = math.factorial(i) - 1
            if num < num_permu:
                permutation_length = i
                break
        return permutation_length

    def get_permutation_map(self,permu_length):
        permu_list=[i for i in range(permu_length)]
        all_permu = list(permutations([permu_list]))
        permu_map={}
        for i in range(len(all_permu)):
            permu_map[i]=all_permu[i]

        return permu_map

    def countLeadingZeros(self,binary):
        num = 0
        cur = 0
        while binary[cur] != '1':
            num += 1
            cur += 1
        return num

    def encodeDeck(self,encode_num, num_leading_zero):
        deck=[i for i in range(52)]
        permu_length=self.get_permutation_length(encode_num)
        permu_map=self.get_permutation_map(permu_length)
        permutation=permu_map[encode_num]
        used_deck=[i for i in range(52-permu_length,52)]
        arrange_used_deck=[]
        for p in permutation:
            arrange_used_deck.append(used_deck[p])

        leading_zero_card=self.zero_permu_map[num_leading_zero]
        unused_deck=deck-leading_zero_card-arrange_used_deck
        final_deck=unused_deck+leading_zero_card+arrange_used_deck


        print(final_deck)
        return final_deck

    def decodeDeck(self, deck):
        count_unused = 0
        start_card = 0
        while (deck[start_card] != 0):
            start_card += 1
            count_unused += 1

        start_group = [0, 1, 2, 3]
        expected_num_unsused = max(deck[:start_card])

        used_deck = []

        for card in deck[start_card:]:
            if card in start_group or card > expected_num_unsused:
                used_deck.append(card)

        #print(used_deck)
        decode_permu = []
        i = 0
        while i < len(used_deck):
            group = (used_deck[i] % 4 + 1, used_deck[i + 1] % 4 + 1, used_deck[i + 2] % 4 + 1, used_deck[i + 3] % 4 + 1)
            print(group)
            i += 4
            for p in self.permu_map:
                if self.permu_map[p] == group:
                    decode_permu.append(p)

        num_leading_zero = decode_permu.pop(0)
        print(num_leading_zero)
        print(decode_permu)

        return num_leading_zero,decode_permu

    def encode(self, message):
        print("message:", message)
        binary = ''
        for letter in message:
            huffman_code = self.huff_LtoB[letter]
            binary += huffman_code

        num_leading_zero = self.countLeadingZeros(binary)

        # print("encode binary:", binary)
        # print("leading zero:",num_leading_zero)
        encode_num = int(binary, 2)
        print("decimal:", encode_num)
        #return encode_num, num_leading_zero
        deck=self.encodeDeck(encode_num, num_leading_zero)

        return deck

    def decode(self, deck):
        num_leading_zero,encode_num=self.decodeDeck(deck)

        decimal_num = self.baseToNumber(encode_num, 24)
        binary_arr = self.numberToBase(decimal_num, 2)
        binary_str = ''.join([str(x) for x in binary_arr])

        add_zero = '0' * num_leading_zero
        final_binary = add_zero + binary_str
        # print(final_binary)

        ans = []
        i = 0
        j = 0
        while j <= len(final_binary):
            if final_binary[i:j] in self.huff_BtoL:
                ans.append(self.huff_BtoL[final_binary[i:j]])
                i = j
            else:
                j += 1

        decode_massage = ''.join(ans)
        print("decode:", decode_massage)

        return decode_massage