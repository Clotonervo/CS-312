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

            matrix = [[(float("inf"), 'X') for j in range(len(sequence2) + 1)] for i in range(len(sequence1) + 1)]
            matrix[0][0] = (0, '$')

        for i in range(len(sequence1) + 1):
            for j in range(len(sequence2) + 1):
                newTuple = self.nextValue(i, j, matrix, sequence1, sequence2)
                if newTuple != 0:
                    matrix[i][j] = newTuple

        bestFit = matrix[len(sequence1)][len(sequence2)][0]
        alignment1, alignment2 = self.getAlignments(matrix, sequence1, sequence2)

        # print("BestFit: ", bestFit, " Alignment1: ", alignment1, " Alignment2: ", alignment2)

        return bestFit, alignment1, alignment2


    def nextValue(self, i, j, matrix, sequence1, sequence2):
        topValue = float("inf")
        leftValue = float("inf")
        diagonalValue = float("inf")
        validOption = False
        leftValid = False
        topValid = False
        diagonalValid = False

        if i - 1 >= 0:
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

            tuple = self.getMin(diagonalValue, topValue, leftValue);
            return tuple
        else:
            return 0

    def getMin(self, diagonal, top, left):

        if diagonal < top and diagonal < left:
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

    def getAlignments(self, matrix, sequence1, sequence2):
        i = len(sequence1)
        j = len(sequence2)
        letterIndex1 = len(sequence1) - 1
        letterIndex2 = len(sequence2) - 1
        currentAlignment1 = ""
        currentAlignment2 = ""
        currentTuple = matrix[i][j]

        while currentTuple[1] != '$':
            if currentTuple[1] == "T":
                currentAlignment2 = "-" + currentAlignment2
                currentAlignment1 = sequence1[letterIndex1] + currentAlignment1
                letterIndex1 -= 1
                i = i - 1
            elif currentTuple[1] == "L":
                currentAlignment1 = "-" + currentAlignment1
                currentAlignment2 = sequence1[letterIndex2] + currentAlignment2
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




    def bandwidthSequenceAlgorithm(self, sequence1, sequence2, align_length):
        if sequence1 == sequence2:
            return MATCH * len(sequence1), sequence1, sequence2
        else:
            k = 7;

            sequence1 = sequence1[:align_length]
            sequence2 = sequence2[:align_length]

            if abs(len(sequence1) - len(sequence2)) > 3:
                # print("Sequence 1 length: ", len(sequence1), "/n Sequence 2 length: ", len(sequence2))
                return float("inf"), "", ""

            sequence1 = sequence1[:align_length]
            sequence2 = sequence2[:align_length]

            if (len(sequence2) > len(sequence1)):
                temp = sequence2
                sequence2 = sequence1
                sequence1 = temp

            matrix = [[(float("inf"), 'X') for j in range(k)] for i in range(len(sequence1) + 1)]
            matrix[0][0] = (0, '$')
            for i in range(len(sequence1) + 1):
                for j in range(len(sequence2) + 1):
                    if i - j > 3:
                        continue
                    elif j - i > 3:
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

            for j in range(k):
                if matrix[len(sequence1)][j][0] == float("inf"):
                    bestFit = matrix[len(sequence1)][j - 1][0]
                    indexOfBestFit = j - 1
                    break

            # print(bestFit)
            alignment1, alignment2 = self.getBandwidthAlignments(matrix, sequence1, sequence2, indexOfBestFit)

            return bestFit, alignment1, alignment2


    def bandedNextValue(self, i, j, matrix, sequence1, sequence2):
        topValue = float("inf")
        leftValue = float("inf")
        diagonalValue = float("inf")
        validOption = False
        leftValid = False
        topValid = False
        diagonalValid = False

        shiftedI = i - 3

        if i - 1 >= 0 and j - shiftedI + 1 < 7:
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
                if sequence1[i -1] == sequence2[j-1]:
                    diagonalValue = diagonalValue + MATCH
                else:
                    diagonalValue = diagonalValue + SUB

            if topValid:
                topValue = topValue + INDEL

            if leftValid:
                leftValue = leftValue + INDEL

            tuple = self.getMin(diagonalValue, topValue, leftValue);
            return tuple
        else:
            return 0


    def getBandwidthAlignments(self, matrix, sequence1, sequence2, indexOfBestFit):
        i = len(sequence1)
        j = indexOfBestFit
        letterIndex1 = len(sequence1) - 1
        letterIndex2 = len(sequence2) - 1
        currentAlignment1 = ""
        currentAlignment2 = ""
        currentTuple = matrix[i][j]

        while currentTuple[1] != '$':
            if i <= 3:
                subString1 = sequence1[:(letterIndex1 + 1)]
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
                currentAlignment2 = sequence1[letterIndex2] + currentAlignment2
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

