
def getClosestRightPoint(points)
    return points[length(points)]


def getClosestLeftPoint(points)
    return points[0]

def getUpperTangent(leftPoint, rightPoint, leftList, rightList)
    leftStart = leftPoint
    rightStart = rightStart


    

    return


def merge(leftSide, rightSide):
    leftPoint = rightSide.index(getClosestLeftPoint(rightSide))
    rightPoint = leftSide.index(getClosestRightPoint(leftSide))



    print("In the Merge algorithm")
    return




def divideAndConquer(sortedPoints):
    if length(sortedPoints) < 4:        # This will mean that when there are only 3 or less points will we start combining
        return sortedPoints
    else:
        leftSide = divideAndConquer([:len(sortedPoints)//2])
        rightSide = divideAndConquer([len(sortedPoints)//2:])

        return merge(leftSide, rightSide)


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
        sortedList = sorted(self.points , key=lambda k: k.x())  # Python sorted function
        t2 = time.time()
        print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2-t1))

        t3 = time.time()
        divideAndConquer()
        t4 = time.time()

        USE_DUMMY = True
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
