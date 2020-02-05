# Fails on 10 points on seed 0

def divideAndConquer(self, sortedPoints):
    print("***********************")
    print("sortedPoints = ", len(sortedPoints))
    if len(sortedPoints) < 4:        # This will mean that when there are only 3 or less points will we start combining
        return sortedPoints
    else:
        leftSide = divideAndConquer(self, sortedPoints[:len(sortedPoints)//2])
        rightSide = divideAndConquer(self, sortedPoints[len(sortedPoints)//2:])

        print("leftSide = ", len(leftSide))
        print("rightSide = ", len(rightSide))

        return merge(self, leftSide, rightSide)



def getClosestRightPoint(points):
        index = 0;
        xPoint = points[0].x();
        for i in range(len(points)):
            if (points[i].x() > xPoint):
                xPoint = points[i].x()
                index = i
        return index


def getClosestLeftPoint(points):
    index = 0;
    xPoint = points[0].x();
    for i in range(len(points)):
        if (points[i].x() < xPoint):
            xPoint = points[i].x()
            index = i
    return index

def getUpperTangent(self, leftStart, rightStart, leftList, rightList):
    currentSlope = getSlope(leftList[leftStart], rightList[rightStart])
    rightLength = len(rightList)
    leftLength = len(leftList)
    slopeIncreasing = True
    slopeDecreasing = True
    currentRightTangent = rightStart
    currentLeftTangent = leftStart
    leftPoint = leftStart
    rightPoint = rightStart
    # print("Initial LeftPoint = ", leftPoint)
    # print("Initial RightPoint = ", rightPoint)
    # print("Initial Slope = ", currentSlope)

    # polygonLeft = [QLineF(leftList[leftStart], rightList[rightStart])]
    # assert( type(polygonLeft) == list and type(polygonLeft[0]) == QLineF )
    # self.show_hull.emit(polygonLeft,(0,0,0))

    while True:
        slopeIncreasing = True
        slopeDecreasing = True

        while slopeIncreasing:
            nextPointSlope = getSlope(leftList[leftPoint], rightList[(rightPoint + 1) % rightLength])
            # print("nextPointSlope = ", nextPointSlope)

            if nextPointSlope > currentSlope:
                currentSlope = nextPointSlope
                rightPoint = (rightPoint + 1) % rightLength
                slopeIncreasing = True

            else:
                slopeIncreasing = False

        # return currentLeftTangent, rightPoint
        # print("now Slope = ", currentSlope)

        while slopeDecreasing:
            nextPointSlope = getSlope(leftList[(leftPoint - 1) % leftLength], rightList[rightPoint])

            if nextPointSlope < currentSlope:
                currentSlope = nextPointSlope;
                leftPoint = (leftPoint - 1) % leftLength
                slopeDecreasing = True

            else:
                slopeDecreasing = False

        # return leftPoint, rightPoint
        # print("LeftPoint = ", leftPoint)
        # print("RightPoint = ", rightPoint)

        if (rightPoint == currentRightTangent) and (leftPoint == currentLeftTangent):
            # print("not looping again")
            return leftPoint, rightPoint
        else:
            # print("looping again in upper tangent")

            currentRightTangent = rightPoint
            currentLeftTangent = leftPoint

def getLowerTangent(self, leftStart, rightStart, leftList, rightList):
    # print("****************************")
    currentSlope = getSlope(leftList[leftStart], rightList[rightStart])
    rightLength = len(rightList)
    leftLength = len(leftList)
    slopeIncreasing = True
    slopeDecreasing = True
    currentRightTangent = rightStart
    currentLeftTangent = leftStart
    leftPoint = leftStart
    rightPoint = rightStart

    # print("Initial LeftPoint = ", leftStart)
    # print("Initial RightPoint = ", rightStart)
    # print("Initial Slope = ", currentSlope)
    #
    # polygonLeft = [QLineF(leftList[leftStart], rightList[rightStart])]
    # assert( type(polygonLeft) == list and type(polygonLeft[0]) == QLineF )
    # self.show_hull.emit(polygonLeft,(0,0,0))

    while True:
        slopeIncreasing = True
        slopeDecreasing = True

        while slopeDecreasing:
            nextPointSlope = getSlope(leftList[leftPoint], rightList[(rightPoint - 1) % rightLength])
            # print("nextPointSlope = ", nextPointSlope)

            if nextPointSlope < currentSlope:
                currentSlope = nextPointSlope
                rightPoint = (rightPoint - 1) % rightLength
                slopeDecreasing = True

            else:
                slopeDecreasing = False

        # return currentLeftTangent, rightPoint
        # print("now Slope = ", currentSlope)

        while slopeIncreasing:
            nextPointSlope = getSlope(leftList[(leftPoint + 1) % leftLength], rightList[rightPoint])

            if nextPointSlope > currentSlope:
                currentSlope = nextPointSlope;
                leftPoint = (leftPoint + 1) % leftLength
                slopeIncreasing = True

            else:
                slopeIncreasing = False

        # return leftPoint, rightPoint
        # print("LeftPoint = ", leftPoint)
        # print("RightPoint = ", rightPoint)

        if (rightPoint == currentRightTangent) and (leftPoint == currentLeftTangent):
            # print("not looping again")
            return leftPoint, rightPoint
        else:
            # print("looping again in upper tangent")

            currentRightTangent = rightPoint
            currentLeftTangent = leftPoint



def getSlope(A, B):
    return (A.y() - B.y())/(A.x() - B.x())


# def orderClockwise(pointsList):
#     if (getSlope(pointsList[0], pointsList[1]) >= getSlope(pointsList[0], pointsList[2])):
#         return pointsList
#     else:
#         newPointsList = [pointsList[0], pointsList[2], pointsList[1]]
#         return newPointsList

def orderClockwise(pointList):
    leftMostXIndex = getClosestLeftPoint(pointList)
    rightMostXIndex = getClosestRightPoint(pointList)
    leftMostX = pointList[leftMostXIndex]
    rightMostX = pointList[rightMostXIndex]

    print("rightMostPoint = ", rightMostXIndex)
    print("leftMostPoint = ", leftMostXIndex)


    currentIndex = 0

    for p in pointList:
        if p != leftMostX and p != rightMostX:
            heightDiff = leftMostX.y() - rightMostX.y()
            if p.y() < leftMostX.y():
                print("current Index = ", currentIndex)
                newPointsList = [pointList[leftMostXIndex], pointList[rightMostXIndex], pointList[currentIndex]]
                print("returning: ",leftMostXIndex, rightMostXIndex, currentIndex)
                return newPointsList
            else:
                print("current Index = ", currentIndex)
                newPointsList = [pointList[leftMostXIndex], pointList[currentIndex], pointList[rightMostXIndex]]
                print("returning: ",leftMostXIndex, currentIndex, rightMostXIndex)
                return pointList
        currentIndex += 1



def merge(self, leftSide, rightSide):
    # print("In the Merge algorithm")
    print("leftSide unsorted = ", leftSide)
    print("rightSide unsorted = ", rightSide)

    if len(leftSide) < 4 or len(rightSide) < 4:
        if len(leftSide) == 3:
            leftSide = orderClockwise(leftSide)
        if len(rightSide) == 3:
            rightSide = orderClockwise(rightSide)

    print("leftSide = ", leftSide)
    print("rightSide = ", rightSide)

#Show left shape
    polygonLeft = [QLineF(leftSide[i],leftSide[(i+1)%len(leftSide)]) for i in range(len(leftSide))]
    assert( type(polygonLeft) == list and type(polygonLeft[0]) == QLineF )
    self.show_hull.emit(polygonLeft,(0,0,255))

# #show right shape
    polygonRight = [QLineF(rightSide[i],rightSide[(i+1)%len(rightSide)]) for i in range(len(rightSide))]
    assert( type(polygonRight) == list and type(polygonRight[0]) == QLineF )
    self.show_hull.emit(polygonRight,(0,255,0))

    leftStart = getClosestRightPoint(leftSide)
    rightStart = getClosestLeftPoint(rightSide)

    leftTopTangent, rightTopTangent = getUpperTangent(self, leftStart, rightStart, leftSide, rightSide)
    # print(leftTopTangent)
    # print(rightTopTangent)
    # upperTangent = [QLineF(leftSide[leftTopTangent], rightSide[rightTopTangent])]
    # assert( type(upperTangent) == list and type(upperTangent[0]) == QLineF )
    # self.show_hull.emit(upperTangent,(255,0,0))

    leftBottomTangent, rightBottomTangent = getLowerTangent(self, leftStart, rightStart, leftSide, rightSide)
    #
    # lowerTangent = [QLineF(leftSide[leftBottomTangent], rightSide[rightBottomTangent])]
    # assert( type(lowerTangent) == list and type(lowerTangent[0]) == QLineF )
    # self.show_hull.emit(lowerTangent,(255,0,0))


    side = [QLineF(leftSide[0], rightSide[0])]
    assert( type(side) == list and type(side[0]) == QLineF )
    self.show_hull.emit(side,(0,0,0))

    side = [QLineF(leftSide[1], rightSide[1])]
    assert( type(side) == list and type(side[0]) == QLineF )
    self.show_hull.emit(side,(0,0,0))

    # side = [QLineF(leftSide[2], rightSide[2])]
    # assert( type(lowerTangent) == list and type(side[0]) == QLineF )
    # self.show_hull.emit(side,(0,0,0))

    print("leftTopTangent = ", leftTopTangent, " ", leftSide[leftTopTangent])
    print("rightTopTangent = ", rightTopTangent, " ", rightSide[rightTopTangent])
    print("leftBottomTangent = ", leftBottomTangent, " ", leftSide[leftBottomTangent])
    print("rightBottomTangent = ", rightBottomTangent, " ", rightSide[rightBottomTangent])


    endList = []
    # endList.append(rightSide[rightTopTangent])
    i = rightTopTangent

    if rightTopTangent != rightBottomTangent:
         while i != rightBottomTangent:
            endList.append(rightSide[i])
            i = (i + 1) % len(rightSide)
         endList.append(rightSide[rightBottomTangent])
    else:
         endList.append(rightSide[rightTopTangent])



    if leftTopTangent != leftBottomTangent:
        i = leftBottomTangent
        while i != leftTopTangent:
            endList.append(leftSide[i])
            i = (i + 1) % len(leftSide)
        endList.append(leftSide[leftTopTangent])
    else:
        endList.append(leftSide[leftBottomTangent])

    # if leftTopTangent != leftBottomTangent:
    #     while i != leftTopTangent:
    #         endList.append(leftSide[i])
    #         i = (i + 1) % len(leftSide)
    #     endList.append(leftSide[leftTopTangent])
    # else:
    #     endList.append(leftSide[leftBottomTangent])
    #
    # i = rightTopTangent
    #
    # if rightTopTangent != rightBottomTangent:
    #      while i != rightBottomTangent:
    #         endList.append(rightSide[i])
    #         i = (i + 1) % len(rightSide)
    #      endList.append(rightSide[rightBottomTangent])
    # else:
    #      endList.append(rightSide[rightTopTangent])



    # while i != leftTopTangent:
    #     endList.append(rightSide[i])
    #     i = (i + 1) % len(rightSide)

    # endList.append(rightSide[rightBottomTangent])
    # # endList.append(leftSide[leftBottomTangent])
    # i = leftBottomTangent
    #
    # while i != leftTopTangent:
    #     endList.append(leftSide[i])
    #     i = (i + 1) % len(leftSide)
    # endList.append(leftSide[leftTopTangent])

    print("endList = ", endList)


    return endList





from PyQt5.QtCore import QLineF, QPointF, QThread, pyqtSignal



import time



class ConvexHullSolverThread(QThread):
    def __init__( self, unsorted_points,demo):
        self.points = unsorted_points
        self.pause = demo
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    # These two signals are used for interacting with the GUI.
    show_hull    = pyqtSignal(list,tuple)
    display_text = pyqtSignal(str)

    # Some additional thread signals you can implement and use for debugging,
    # if you like
    show_tangent = pyqtSignal(list,tuple)
    erase_hull = pyqtSignal(list)
    erase_tangent = pyqtSignal(list)


    def set_points( self, unsorted_points, demo):
        self.points = unsorted_points
        self.demo   = demo



    def run(self):
        assert( type(self.points) == list and type(self.points[0]) == QPointF )

        n = len(self.points)
        print( 'Computing Hull for set of {} points'.format(n) )

        t1 = time.time()
        self.points = sorted(self.points , key=lambda k: k.x())  # Python sorted function
        t2 = time.time()
        print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2-t1))

        t3 = time.time()
        finalList = divideAndConquer(self, self.points)
        t4 = time.time()

        polygon = [QLineF(finalList[i],finalList[(i+1)%len(finalList)]) for i in range(len(finalList))]
        assert( type(polygon) == list and type(polygon[0]) == QLineF )
        self.show_hull.emit(polygon,(255,255,255))


        USE_DUMMY = False
        if USE_DUMMY:
            # This is a dummy polygon of the first 3 unsorted points
            polygon = [QLineF(self.points[i],self.points[(i+1)%3]) for i in range(3)]

            # When passing lines to the display, pass a list of QLineF objects.
            # Each QLineF object can be created with two QPointF objects
            # corresponding to the endpoints
            assert( type(polygon) == list and type(polygon[0]) == QLineF )

            # Send a signal to the GUI thread with the hull and its color
            self.show_hull.emit(polygon,(0,255,0))

        else:
            # TODO: PASS THE CONVEX HULL LINES BACK TO THE GUI FOR DISPLAY
            pass


        # Send a signal to the GUI thread with the time used to compute the
        # hull
        self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
        print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
