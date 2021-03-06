
#   divideAndConquer()
#   Time: O(nlog(n)), because a = 2, b = 2, and d = 1, which leaves us with O(nlog(n)) according to the master's theorm
#   Space: O(nlog(n)), gets called log(n) times in recursion, each time storing a list with size n, so ends up being a total of O(nlog(n))
def divideAndConquer(sortedPoints):
    if len(sortedPoints) < 3:        # This will mean that when there are only 2 or less points will we start combining
        return sortedPoints
    else:
        leftSide = divideAndConquer(sortedPoints[:len(sortedPoints)//2])
        rightSide = divideAndConquer(sortedPoints[len(sortedPoints)//2:])
        return merge(leftSide, rightSide)

#   getSlope()
#   Time: O(1)
#   Space: O(1)
def getSlope(A, B):
    return (A.y() - B.y())/(A.x() - B.x())  #returns the slope between A and B

#   getClosestRightPoint()
#   Time: O(n), loops through each element in points
#   Space: O(1), No recursion, stored variables are small in comparison
def getClosestRightPoint(points):
    index = 0;
    xPoint = points[0].x();
    for i in range(len(points)):        #Loops through each element to find leftMostX
        if (points[i].x() > xPoint):
            xPoint = points[i].x()
            index = i
    return index

#   getClosestLeftPoint()
#   Time: O(n), loops through each element in points
#   Space: O(1), No recursion, stored variables are small in comparison
def getClosestLeftPoint(points):
    index = 0;
    xPoint = points[0].x();
    for i in range(len(points)):         #Loops through each element to find leftMostX
        if (points[i].x() < xPoint):
            xPoint = points[i].x()
            index = i
    return index

#   getUpperTangent()
#   Time: O(n), worst case scenario we loop through each node in the two lists
#   Space: O(1), it is constant because it simply returns two values
def getUpperTangent(leftStart, rightStart, leftList, rightList):
    currentSlope = getSlope(leftList[leftStart], rightList[rightStart])
    rightLength = len(rightList)
    leftLength = len(leftList)
    slopeIncreasing = True
    slopeDecreasing = True
    currentRightTangent = rightStart
    currentLeftTangent = leftStart
    leftPoint = leftStart
    rightPoint = rightStart

    while True:                         # This only loops when a change is found, still O(n) time;
        slopeIncreasing = True          # Two steps both with O(n), which comes to O(n) total time
        slopeDecreasing = True

        while slopeIncreasing:                      # Starts at closest points, follows left point up first
            nextPointSlope = getSlope(leftList[leftPoint], rightList[(rightPoint + 1) % rightLength])

            if nextPointSlope > currentSlope:        # At worst case loops through each point, but is still O(n)
                currentSlope = nextPointSlope
                rightPoint = (rightPoint + 1) % rightLength
                slopeIncreasing = True
            else:
                slopeIncreasing = False

        while slopeDecreasing:              # Now starts at left point and rotates it up until at the top
            nextPointSlope = getSlope(leftList[(leftPoint - 1) % leftLength], rightList[rightPoint])

            if nextPointSlope < currentSlope:        # At worst case loops through each point, but is still O(n)
                currentSlope = nextPointSlope;
                leftPoint = (leftPoint - 1) % leftLength
                slopeDecreasing = True
            else:
                slopeDecreasing = False

        if (rightPoint == currentRightTangent) and (leftPoint == currentLeftTangent):
            return leftPoint, rightPoint
        else:
            currentRightTangent = rightPoint
            currentLeftTangent = leftPoint

#   getLowerTangent()
#   Time: O(n), worst case scenario we loop through each node in the two lists
#   Space: O(1), it is constant because it simply returns two values
def getLowerTangent(leftStart, rightStart, leftList, rightList):
    currentSlope = getSlope(leftList[leftStart], rightList[rightStart])
    rightLength = len(rightList)
    leftLength = len(leftList)
    slopeIncreasing = True
    slopeDecreasing = True
    currentRightTangent = rightStart
    currentLeftTangent = leftStart
    leftPoint = leftStart
    rightPoint = rightStart

    while True:                             # This only loops when a change is found, still O(n) time;
        slopeIncreasing = True              # Two steps both with O(n), which comes to O(n) total time
        slopeDecreasing = True

        while slopeDecreasing:          # Starts at closest points, follows right point down first
            nextPointSlope = getSlope(leftList[leftPoint], rightList[(rightPoint - 1) % rightLength])

            if nextPointSlope < currentSlope:             # At worst case loops through each point, but is still O(n)
                currentSlope = nextPointSlope
                rightPoint = (rightPoint - 1) % rightLength
                slopeDecreasing = True

            else:
                slopeDecreasing = False

        while slopeIncreasing:          # Takes left point and shifts it down clockwise until flatest.
            nextPointSlope = getSlope(leftList[(leftPoint + 1) % leftLength], rightList[rightPoint])

            if nextPointSlope > currentSlope:            # At worst case loops through each point, but is still O(n)
                currentSlope = nextPointSlope;
                leftPoint = (leftPoint + 1) % leftLength
                slopeIncreasing = True

            else:
                slopeIncreasing = False

        if (rightPoint == currentRightTangent) and (leftPoint == currentLeftTangent):
            return leftPoint, rightPoint
        else:
            currentRightTangent = rightPoint
            currentLeftTangent = leftPoint


#   merge()
#   Time: O(n), many of the function calls and other parts of this function are all O(n) time
#   Space: O(n), the end of this function creates a new array of at most n elements
def merge(leftSide, rightSide):
    leftStart = getClosestRightPoint(leftSide)
    rightStart = getClosestLeftPoint(rightSide)

    leftTopTangent, rightTopTangent = getUpperTangent(leftStart, rightStart, leftSide, rightSide)
    leftBottomTangent, rightBottomTangent = getLowerTangent(leftStart, rightStart, leftSide, rightSide)

    endList = []                         # Because there are a few different steps of O(n), the total complexity is still O(n) at worst case
    i = rightTopTangent

    # Starts at top right tangent, and loops around shape clockwise, checking to see if tangents on either side are the same
    if rightTopTangent != rightBottomTangent:           # Worst case loops through each point, O(n)
         while i != rightBottomTangent:
            endList.append(rightSide[i])
            i = (i + 1) % len(rightSide)
         endList.append(rightSide[rightBottomTangent])
    else:
         endList.append(rightSide[rightTopTangent])

    if leftTopTangent != leftBottomTangent:             # Worst case loops through each point, O(n)
        i = leftBottomTangent
        while i != leftTopTangent:
            endList.append(leftSide[i])
            i = (i + 1) % len(leftSide)
        endList.append(leftSide[leftTopTangent])
    else:
        endList.append(leftSide[leftBottomTangent])
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
        self.points = sorted(self.points , key=lambda k: k.x())  # Python sort function, O(nlogn) time, O(n) space
        t2 = time.time()
        print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2-t1))

        t3 = time.time()
        finalList = divideAndConquer(self.points) # This is O(nlogn) time, O(nlog(n)) space at worst case
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
