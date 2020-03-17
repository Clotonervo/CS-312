#!/usr/bin/python3

#from PyQt5.QtCore import QLineF, QPointF
import math
import time

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

    def __init__( self ):
        pass

# This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
# handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
# how many base pairs to use in computing the alignment
    def align( self, sequences, table, banded, align_length ):
        self.banded = banded
        self.MaxCharactersToAlign = align_length
        results = []

        for i in range(len(sequences)):
            jresults = []
            for j in range(len(sequences)):
                if j < i:
                   s = {}
                else:
                    if banded:
                        score, alignment1, alignment2 = self.bandwidthSequenceAlgorithm(sequences[i], sequences[j], align_length)
                    else:
                        score, alignment1, alignment2 = self.sequenceAlgorithm(sequences[i], sequences[j], align_length)

                    s = {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
                    table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
                    table.repaint()
                jresults.append(s)
            results.append(jresults)
        return results

    # Unrestricted Algorithm
    # Time: O(nm) time, to fill up the matrix, and to iterate through each element in the 2d matrix
    # Space: O(nm) space, as we fill up a 2d matrix and alter those values, but it is the only major object we create
    def sequenceAlgorithm(self, sequence1, sequence2, align_length):
        if sequence1 == sequence2:
            return MATCH * len(sequence1), sequence1, sequence2
        else:
            sequence1 = sequence1[:align_length]
            sequence2 = sequence2[:align_length]

            if(len(sequence2) > len(sequence1)):
                temp = sequence2
                sequence2 = sequence1
                sequence1 = temp

            matrix = [[(float("inf"), 'X') for j in range(len(sequence2) + 1)] for i in range(len(sequence1) + 1)] #O(nm) time and space
            matrix[0][0] = (0, '$')

        for i in range(len(sequence1) + 1): #O(nm) time
            for j in range(len(sequence2) + 1):
                newTuple = self.nextValue(i, j, matrix, sequence1, sequence2)
                if newTuple != 0:
                    matrix[i][j] = newTuple

        bestFit = matrix[len(sequence1)][len(sequence2)][0]
        alignment1, alignment2 = self.getAlignments(matrix, sequence1, sequence2)  #O(n) time, with O(n) space for the strings

        return bestFit, alignment1, alignment2

    # Time: O(1), because each lookup is constant, and we have no loops, just lots of
    #      simple comparisions
    # Space: O(1), no objects of length n are created, each value stored is O(1)
    def nextValue(self, i, j, matrix, sequence1, sequence2):
        topValue = float("inf")
        leftValue = float("inf")
        diagonalValue = float("inf")
        validOption = False
        leftValid = False
        topValid = False
        diagonalValid = False

        if i - 1 >= 0:                  # All these comparisons are O(1)
            validOption = True
            topValid = True
            topValue = matrix[i - 1][j][0]
        if j - 1 >= 0:
            validOption = True
            leftValid = True
            leftValue = matrix[i][j - 1][0]
        if i - 1 >= 0 and j - 1 >= 0:
            validOption = True
            diagonalValid = True
            diagonalValue = matrix[i - 1][j - 1][0]

        if validOption:
            if diagonalValid:
                if sequence1[i -1] == sequence2[j-1]:
                    diagonalValue = diagonalValue + MATCH
                else:
                    diagonalValue = diagonalValue + SUB

            if topValid:
                topValue = topValue + INDEL

            if leftValid:
                leftValue = leftValue + INDEL

            tuple = self.getMin(diagonalValue, topValue, leftValue);    #O(1) time and space
            return tuple
        else:
            return 0

    # Time: O(1), these are just simple comparisions to find the minimum value
    # Space: O(1), we only create and store a single tuple which takes O(1) space
    def getMin(self, diagonal, top, left):

        if diagonal < top and diagonal < left:          # All these comparisons are O(1) time and space
            return (diagonal, "D")
        elif top < diagonal and top < left:
            return (top, "T")
        elif left < diagonal and left < top:
            return (left, "L")
        else:
            minValue = min(diagonal, top, left)

            if minValue == diagonal:
                return (diagonal, "D")
            elif minValue == top:
                return (top, "T")
            else:
                return (left, "L")

    # Time: O(n) or O(m), whichever is largest, as we travers back through the 2d matrix
    #       all the way to the upper right corner
    # Space: O(n) or O(m), we store strings of length m and n,
    def getAlignments(self, matrix, sequence1, sequence2):
        i = len(sequence1)
        j = len(sequence2)
        letterIndex1 = len(sequence1) - 1
        letterIndex2 = len(sequence2) - 1
        currentAlignment1 = ""
        currentAlignment2 = ""
        currentTuple = matrix[i][j]

        while currentTuple[1] != '$':           # O(m) or O(n) worst case, as it will traverse through the matrix back
                                                # to the origin
            if currentTuple[1] == "T":          # Each comparison is O(1) time
                currentAlignment2 = "-" + currentAlignment2
                currentAlignment1 = sequence1[letterIndex1] + currentAlignment1
                letterIndex1 -= 1
                i = i - 1
            elif currentTuple[1] == "L":
                currentAlignment1 = "-" + currentAlignment1
                currentAlignment2 = sequence2[letterIndex2] + currentAlignment2
                letterIndex2 -= 1
                j = j - 1
            else:
                currentAlignment1 = sequence1[letterIndex1] + currentAlignment1
                currentAlignment2 = sequence2[letterIndex2] + currentAlignment2
                i = i - 1
                j = j - 1
                letterIndex1 -= 1
                letterIndex2 -= 1
            currentTuple = matrix[i][j]


        return currentAlignment1, currentAlignment2


    #Banded Algorithm
    # Time: O(kn), we iterate through a 2d array of n*k size, so if each element is O(1),
    #   then our time complexity for this algorithm to make the array and iterate through it
    #   is O(kn) time
    # Space: O(kn), to hold a 2d matrix of size k*n
    def bandwidthSequenceAlgorithm(self, sequence1, sequence2, align_length):
        if sequence1 == sequence2:
            return MATCH * len(sequence1), sequence1, sequence2
        else:
            k = 7;

            sequence1 = sequence1[:align_length]
            sequence2 = sequence2[:align_length]

            if abs(len(sequence1) - len(sequence2)) > MAXINDELS:
                return float("inf"), "No Alignment Possible", "No Alignment Possible"

            sequence1 = sequence1[:align_length]
            sequence2 = sequence2[:align_length]

            if (len(sequence2) > len(sequence1)):
                temp = sequence2
                sequence2 = sequence1
                sequence1 = temp

            matrix = [[(float("inf"), 'X') for j in range(k)] for i in range(len(sequence1) + 1)]   #O(kn) time and space for this 2d array
            matrix[0][0] = (0, '$')
            shift = 0
            for i in range(len(sequence1) + 1):     # Loops through k*n times, O(kn) complexity
                if i - (len(sequence1) + 1) >= -3:
                    pass
                elif i > 3:
                    shift += 1
                for j in range(k):
                    j += shift
                    if i - j > 3:               # These comparisions are O(1)
                        continue
                    elif j - i > 3:
                        break
                    elif j > len(sequence2):
                        break

                    if i <= 3:
                        newTuple = self.nextValue(i, j, matrix, sequence1, sequence2)
                        if newTuple != 0:
                            matrix[i][j] = newTuple
                    else:
                        newTuple = self.bandedNextValue(i, j, matrix, sequence1, sequence2)
                        if newTuple != 0:
                            matrix[i][j - (i - 3)] = newTuple

            bestFit = float("inf")
            indexOfBestFit = 0

            for j in range(k):          #O(k) time, but is small compared to O(kn)
                if matrix[len(sequence1)][j][0] == float("inf"):
                    bestFit = matrix[len(sequence1)][j - 1][0]
                    indexOfBestFit = j - 1
                    break

            alignment1, alignment2 = self.getBandwidthAlignments(matrix, sequence1, sequence2, indexOfBestFit)  #O(n) or O(m) time and space
            return bestFit, alignment1, alignment2

    # Time: O(1), because each lookup is constant, and we have no loops, just lots of
    #      simple comparisions
    # Space: O(1), no objects of length n are created, each value stored is O(1)
    def bandedNextValue(self, i, j, matrix, sequence1, sequence2):
        topValue = float("inf")
        leftValue = float("inf")
        diagonalValue = float("inf")
        validOption = False
        leftValid = False
        topValid = False
        diagonalValid = False

        shiftedI = i - 3

        if i - 1 >= 0 and j - shiftedI + 1 < 7:         # comparisions are O(1)
            validOption = True
            topValid = True
            topValue = matrix[i - 1][j + 1 - shiftedI][0]
        if j - shiftedI - 1 >= 0:
            validOption = True
            leftValid = True
            leftValue = matrix[i][j - 1 - shiftedI][0]
        if i - 1 >= 0:
            validOption = True
            diagonalValid = True
            diagonalValue = matrix[i - 1][j - shiftedI][0]

        if validOption:
            if diagonalValid:
                if sequence1[i -1] == sequence2[j - 1]:
                    diagonalValue = diagonalValue + MATCH
                else:
                    diagonalValue = diagonalValue + SUB

            if topValid:
                topValue = topValue + INDEL

            if leftValid:
                leftValue = leftValue + INDEL

            tuple = self.getMin(diagonalValue, topValue, leftValue); #O(1) time and space
            return tuple
        else:
            return 0

    # Time: O(n) or O(m), whichever is largest, as we travers back through the 2d matrix
    #       all the way to the upper right corner
    # Space: O(n) or O(m), we store strings of length m and n,
    def getBandwidthAlignments(self, matrix, sequence1, sequence2, indexOfBestFit):
        i = len(sequence1)
        j = indexOfBestFit
        letterIndex1 = len(sequence1) - 1
        letterIndex2 = len(sequence2) - 1
        currentAlignment1 = ""
        currentAlignment2 = ""
        currentTuple = matrix[i][j]

        while currentTuple[1] != '$':           # Will loop through matrix until gets to origin, O(n) or O(m) complexity
            if i <= 3:
                subString1 = sequence1[:(letterIndex1 + 1)]         # Each of these is O(1)
                subString2 = sequence2[:(letterIndex2 + 1)]
                beginningAlignment1, beginningAlignment2 = self.getAlignments(matrix, subString1, subString2)
                currentAlignment1 = beginningAlignment1 + currentAlignment1
                currentAlignment2 = beginningAlignment2 + currentAlignment2
                break
            if currentTuple[1] == "T":
                currentAlignment2 = "-" + currentAlignment2
                currentAlignment1 = sequence1[letterIndex1] + currentAlignment1
                letterIndex1 -= 1
                i = i - 1
                j = j + 1
            elif currentTuple[1] == "L":
                currentAlignment1 = "-" + currentAlignment1
                currentAlignment2 = sequence2[letterIndex2] + currentAlignment2
                letterIndex2 -= 1
                j = j - 1
            else:
                currentAlignment1 = sequence1[letterIndex1] + currentAlignment1
                currentAlignment2 = sequence2[letterIndex2] + currentAlignment2
                i = i - 1
                letterIndex1 -= 1
                letterIndex2 -= 1
            currentTuple = matrix[i][j]

        return currentAlignment1, currentAlignment2
