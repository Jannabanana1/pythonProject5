# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
"""
import numpy

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def sort_array(matrix):
    newarr = []
    for i in range(len(matrix)):
        arr = numpy.concatenate(matrix[i])
        newarr.append(arr)
    newarr2 = numpy.concatenate(newarr)
    return -numpy.sort(-newarr2)

def POS_tag(sentence):
    punctuation = ".,?/`~!#$%^&*()_-<>"
    lower_sentence = sentence.lower()
    stop = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(lower_sentence)
    #fix string cannot import
    lst = [word for word in tokens if word not in tokens or word not in punctuation]
    tagged = nltk.pos_tag(lst)
    return tagged
"""

class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        "negates the x value of the expression"
        new_lst = []
        for item in self.polynomial:
            item = (item[0], item[1])
            new_lst.append((-item[0], item[1]))
        return Polynomial(new_lst)

    def __add__(self, other):
        new_lst = []
        for item in self.polynomial:
            new_lst.append(item)
        for item2 in other.polynomial:
            new_lst.append(item2)
        return Polynomial(new_lst)

    def __sub__(self, other):
        new_lst = []
        for item in self.polynomial:
            new_lst.append(item)
        for o in other.polynomial:
            o = (-o[0], o[1])
            new_lst.append(o)
        return Polynomial(new_lst)

    def __mul__(self, other):
        new_lst = []
        new_tuple = ()
        new_tuple2 = ()
        new_tuple += (self.polynomial[0][0]*other.polynomial[0][0], self.polynomial[0][1]+other.polynomial[0][1])
        new_tuple2 += (self.polynomial[0][0]*other.polynomial[1][0], self.polynomial[0][1]+other.polynomial[1][1])
        new_lst.append(new_tuple)
        new_lst.append(new_tuple2)
        other_tuple = (self.polynomial[1][0]*other.polynomial[0][0], self.polynomial[1][1]+other.polynomial[0][1])
        other_tuple2 = (self.polynomial[1][0]*other.polynomial[1][0], self.polynomial[1][1]+other.polynomial[1][1])
        new_lst.append(other_tuple)
        new_lst.append(other_tuple2)
        return Polynomial(new_lst)

    def __call__(self, x):
        return sum([item[0]*x**item[1] for item in self.polynomial])


    def simplify(self):
        new_tuple = ()
        dict = {}
        for item in self.polynomial:
#1) combine terms with common power
#check if power in dictionary already, if not we add it to dict
            if item[1] not in dict.keys():
                dict[item[1]] = item[0]
#checks if item exists in dictionary
            else:
                dict[item[1]] = dict.get(item[1]) + item[0]
#adds coefficients if same power
            if (dict.get(item[1]) == 0):
                dict.pop(item[1])
#removes terms with coefficents of zero
        if 0 in dict.values():
            dict.pop(0)

#if all coefficients are cancelled then return 0,0 as tuple
        if len(dict) == 0:
            t = (0, 0)
            new_tuple += (t,)
        else:
#sorts dictionary in descending order of power
            sorted_dict = sorted(dict.items(),
            key=lambda x: x[0], reverse=True)

#creates new tuple that is sorted according to power
            for item in sorted_dict:
                t = (item[1], item[0])
                new_tuple += (t,)
        self.polynomial = new_tuple
        return new_tuple

    def __str__(self):
        cnt = 0
# Take an empty string
        result = ''
        sign = ''
        base = ''
# Loop through each tuple in the list
        for t in self.polynomial:
# Get the sign by checking if first coefficient and if neg or +
            if t[0] < 0 and cnt!= 0:
                sign = '-'
            elif t[0] >= 0 and cnt!=0:
                sign = '+'
#if coefficient not 0 or 1, do not write it out
            if t[0] != 1 and t[0] != -1:
                if cnt != 0:
                    base = abs(t[0])
                else:
                    base = t[0]
            elif t[0] == -1 and t[1] != 0:
                base = '-'
            elif t[0] == -1 and t[1] == 0:
                base = '1'
            elif t[0] == 1 and t[1] == 0:
                base = 1
            else:
                base = ''
# Check for the power
            if t[1] == 0:
#f formats the string and replaces the brackets
                result += f" {sign} {base}"
            elif t[1] == 1:
                result += f" {sign} {base}x"
            else:
                result += f" {sign} {base}x^{t[1]}"
            cnt = cnt + 1
# Return the result after removing the spaces from the front
        result = result.strip()
        return result
    def __repr__(self):
        return str(self)


def digits_to_words(text):
    output = ""
    for i in text:
        if (i == '1'):
            output += "one "
        elif (i == '2'):
            output += "two "
        elif (i == '3'):
            output += "three "
        elif (i == '4'):
            output += "four "
        elif (i == '5'):
            output += "five "
        elif (i == '6'):
            output += "six "
        elif (i == '7'):
            output += "seven "
        elif (i == '8'):
            output += "eight "
        elif (i == '9'):
            output += "nine "
        elif (i == '0'):
            output += "zero "
    output = output.strip()
    print(output)
    return output

def run():
    p = Polynomial([(3, 3), (2, 2), (4,1), (5,0)])
    print([p(x) for x in range(3)])
    #[0, -6, -20, -42, -72]


if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
