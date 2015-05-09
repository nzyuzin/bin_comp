#!/usr/bin/python

from heapq import nlargest
import sys
import struct

class Counter(dict):
    def __missing__(self, key):
        return 0

'''
  data is list of words each word is of the same size
'''
def compress(data, wordSize):
    frequencyTable = Counter()
    for index, word in enumerate(data):
        if index == len(data) - 1:
            break
        nextWord = data[index + 1]
        wordsTuple = (word, nextWord)
        frequencyTable[wordsTuple] = frequencyTable[wordsTuple] + 1
    mostFrequentPairs = nlargest(2 ** wordSize, frequencyTable, key=frequencyTable.get)
    result = []
    skipNextIteration = False
    for i in range(0, len(data) - 1):
        if skipNextIteration:
            skipNextIteration = False
            continue
        word = data[i]
        nextWord = data[i + 1]
        wordsTuple = (word, nextWord)
        if wordsTuple in mostFrequentPairs:
            result += ['1' +
                    bin(mostFrequentPairs.index(wordsTuple))[2:].zfill(wordSize)]
            skipNextIteration = True
        else:
            result += ['0' + word]
    return result

def get_bits(filename):
    result = ''
    def bits(f):
        bytes = (ord(b) for b in f.read())
        for b in bytes:
            for i in xrange(8):
                yield (b >> i) & 1
    for b in bits(open(filename, 'r')):
        result += str(b)
    return result

def make_words(bits, wordSize):
    return [bits[i:i + wordSize] for i in range(0, len(bits), wordSize)]

'''
Takes file to compress as first command line argument and starting word length
as second
'''
if __name__ == '__main__':
    filename = sys.argv[1]
    wordLen = int(sys.argv[2])
    bits = get_bits(filename)
    data = make_words(bits, wordLen)
    print('Initial length of data: ' + str(len(data)))

    previousCompression = data
    thisCompression = compress(data, wordLen)
    compression = 1 - float(len(thisCompression)) / float(len(previousCompression))
    iteration = 1

    print("iteration = " + str(iteration) + " with compression = " +
            str(compression) + " compressed length = " +
            str(len(thisCompression)))
    while compression > 0.17 and len(thisCompression) > 2 ** (wordLen +
            iteration):
        previousCompression = thisCompression
        thisCompression = compress(previousCompression, wordLen + iteration)
        compression = 1 - float(len(thisCompression)) / float(len(previousCompression))
        iteration += 1
        print("iteration = " + str(iteration) + " with compression = " +
                str(compression) + " compressed length = " +
                str(len(thisCompression)))

    print("Data length = " + str(len(data)) + " compressed length = " +
            str(len(thisCompression)) + " iterations = " + str(iteration))
    with open('data.bin', 'wb') as output:
        output.write(bytearray(int(i, 2) for i in
            make_words("".join(thisCompression), 8)))

