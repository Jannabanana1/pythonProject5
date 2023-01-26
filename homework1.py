import nltk
import numpy
############################################################
# CIS 521: Homework 1
############################################################
from nltk.corpus import stopwords

student_name = "Jannatul Ferdaus"

# This is where your grade report will be sent.
student_email = "ferdausj@seas.upenn.edu"

############################################################
# Section 1: Python Concepts
############################################################
"""

python_concepts_question_1 = "Python is strongly typed
which means every object has a fixed type and the interpreter
does not allow things incompatible with that type. For example,
a string cannot be added to a int value such as this: "string" + 2.
This will cause error. Python is dynamically typed which means
variables are assigned their type when you declare them.
For example: x = 'string' declares that x is a string.
But you can update this to be a numerical type by doing x = 2."

python_concepts_question_2 = "The reason is because lists are
unhashable which means they are mutable and we are creating a
dictionary so we must store keys in the dictionary that will
not change but the values can be updated and changed.
Therefore we must change it in this way:
Points_to_names = {"home":[0, 0] , "school":[1, 2], "market":[-1, 1] }
If we make the string the key and the list the value, this
makes it work better with no error."

python_concepts_question_3 = "The join method is much better and
only takes O(n) time complexity because there are n strings.
The for loop method has a list of length M and length strings of N which
makes O(N^2) time."
"""


############################################################
# Section 2: Working with Lists
############################################################


def extract_and_apply(lst, p, f):
    return [f(x) for x in lst if p(x)]


def concatenate(seqs):
    return [num for lst in seqs for num in lst]


def transpose(matrix):
    sublst = []
    transposedlst = []
    row = 0
    column = 0
    lenOfCol = len(matrix[0])
    numRows = len(matrix)

    while ((column != lenOfCol) and (row != len(matrix))):
        sublst.append(matrix[row][column])
        row = row + 1
        if row == len(matrix):
            transposedlst.append(sublst)
            sublst = []  # create new lst
            if (column == lenOfCol) and (row == len(matrix)):
                return
            else:
                column = column + 1
                row = 0
    return transposedlst


############################################################
# Section 3: Sequence Slicing
############################################################


def copy(seq):
    x = seq[::]
    return x


def all_but_last(seq):
    if (len(seq) == 0):
        return seq
    newSeq = seq[:len(seq) - 1]
    return newSeq


def every_other(seq):
    newlst = seq[::2]
    return newlst


############################################################
# Section 4: Combinatorial Algorithms
############################################################


def prefixes(seq):
    prefixlst = []
    index = 0
    if (len(seq) == 0):
        sublist = seq[0:index]
        yield sublist
        prefixlst.append(list(sublist))
        return sublist
    while (True):
        sublist = seq[0:index]
        yield sublist
        prefixlst.append(list(sublist))
        # DID I DO THIS GENERATOR PART CORRECT??
        # yield prefixlst
        index += 1
        if (len(sublist) != 0):
            list(sublist)
            if (sublist == seq):
                break


def suffixes(seq):
    suffixlst = []
    index = 0
    # seq2 = list(seq)
    # print(seq2, "seq2")
    while (True):
        newsublst = seq[index:len(seq)]
        yield newsublst
        suffixlst.append(list(newsublst))
        # DID I DO THIS GENERATOR PART CORRECT??
        index += 1
        if (index == len(seq) + 1):
            break


def slices(seq):
    sets = []
    subset = []
    set2 = []
    prefixlst = list(prefixes(seq))
    suffixlst = list(suffixes(seq))
    # checks if string and returns true if so
    res = isinstance(seq, str)
    if (res is False):
        for item in seq:
            subset.append(item)
            set2.append(subset)
            subset = []
    # this is to make the set from alphabet
    else:
        set2 = list(seq)
    combolist = prefixlst + suffixlst + set2
    # set(tuple(row) for row in prefixlst)
    for item in combolist:
        # ensures not empty list or empty string
        if item not in sets and item != [] and item != '':
            yield item
            sets.append(item)


############################################################
# Section 5: Text Processing
############################################################


def normalize(text):
    sentence = text.strip()
    splitsentence = sentence.split()
    newsentence = " ".join(splitsentence)
    newsentence = newsentence.lower()
    return newsentence


def no_vowels(text):
    without_vowels = ""
    for i in text:
        if ('a' == i.lower() or 'e' == i.lower()
                or 'i' == i.lower() or 'o' == i.lower()
                or 'u' == i.lower()):
            pass
        else:
            without_vowels += i
    return without_vowels


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
    return output


def to_mixed_case(name):
    output = ""
    name = name.strip("_")
    name = name.split("_")
    cnt = 0
    for item in name:
        if (item != '' or item != '' or
                item != "" or item.isspace()):
            if cnt == 0:
                firstword = item[0:].lower()
                output += firstword
                cnt = cnt + 1
            else:
                letter = item[0].upper()
                rest = item[1:].lower()
                cnt = cnt + 1
                output += letter
                output += rest
    return output


############################################################
# Section 6: Polynomials
############################################################


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
        for s in self.polynomial:
            for t in other.polynomial:
                new_tuple += (s[0] * t[0], s[1] + t[1])

                new_lst.append(new_tuple)
                new_tuple = ()
        return Polynomial(new_lst)

    def __call__(self, x):
        return sum([item[0] * x ** item[1] for item in self.polynomial])


def simplify(self):
    new_tuple = ()
    dict = {}
    sorted_dict = {}
    for item in self.polynomial:
        if item[1] not in dict.keys():
            dict[item[1]] = item[0]
        else:
            dict[item[1]] = dict.get(item[1]) + item[0]
        if (dict.get(item[1]) == 0):
            dict.pop(item[1])
    if 0 in dict.values():
        dict.pop(0)
    if len(dict) == 0:
        t = (0, 0)
        new_tuple += (t,)
    else:
        sorted_dict = sorted(dict.items(),
                             key=lambda x: x[0], reverse=True)
    for item in sorted_dict:
        t = (item[1], item[0])
        new_tuple += (t,)
    self.polynomial = new_tuple
    return new_tuple


def __str__(self):
    cnt = 0
    result = ''
    sign = ''
    base = ''
    for t in self.polynomial:
        if t[0] < 0 and cnt != 0:
            sign = '-'
        elif t[0] >= 0 and cnt != 0:
            sign = '+'
        if t[0] != 1 and t[0] != -1:
            if cnt != 0:
                base = abs(t[0])
            else:
                base = t[0]
        elif t[0] == -1 and t[1] != 0:
            base = '-'
        # below was added
        elif t[0] == -1 and t[1] == 0 and cnt == 0:
            base = '-1'
        elif t[0] == 1 and t[1] == 0:
            base = 1
        elif t[0] == -1 and t[1] == 0 and cnt != 0:
            base = 1
        else:
            base = ''
        if t[1] == 0:
            result += f" {sign} {base}"
        elif t[1] == 1:
            result += f" {sign} {base}x"
        else:
            result += f" {sign} {base}x^{t[1]}"
        cnt = cnt + 1
    result = result.strip()
    return result


############################################################
# Section 7: Python Packages
############################################################

"""
def sort_array(list_of_matrices):
    newarr = []
    for i in range(len(list_of_matrices)):
        arr = numpy.concatenate(list_of_matrices[i])
        newarr.append(arr)
    newarr2 = numpy.concatenate(newarr)
    newarr2 = -numpy.sort(-newarr2)
    endarray = numpy.array(newarr2)
    return endarray
"""


def sort_array(list_of_matrices):
    end_result = []
    for i in range(len(list_of_matrices)):
        if (list_of_matrices[i].ndim > 2):
            new_lst = numpy.concatenate(list_of_matrices[i])
        else:
            new_lst = list_of_matrices[i]
        for j in range(len(new_lst)):
            if (new_lst[j].ndim > 1):
                lst = numpy.concatenate(new_lst[j])
                end_result.append(lst)
            else:
                end_result.append(new_lst[j])
    concatenated_lst = numpy.concatenate(end_result)
    end_lst = -numpy.sort(-concatenated_lst)
    end_lst = numpy.array(end_lst)
    return end_lst


def POS_tag(sentence):
    punctuation = ".,?/`~!#$%^&*()_-<>"
    lower_sentence = sentence.lower()
    stop = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(lower_sentence)
    lst = [word for word in tokens
           if word not in stop and word not in punctuation]
    tagged = nltk.pos_tag(lst)
    return tagged


############################################################
# Section 8: Feedback
############################################################


feedback_question_1 = """ I spent about 20 hours on this assignment """

feedback_question_2 = """
I found using yield and generators the most confusing.
I had trouble downloading the new packages as well. """

feedback_question_3 = """ The parts of this assignment that I liked """


def run():
    matrix1 = numpy.array([[1, 2], [3, 4]])
    matrix2 = numpy.array([ [[[5, 6, 7]], [[7, 8, 9]], [[0, -1, -2]]],[[[5, 6, 7]], [[7, 8, 9]], [[0, -1, -2]]]])
    print(sort_array([matrix1, matrix2]))


if __name__ == '__main__':
    run()
