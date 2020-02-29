#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__( self ):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

# Time: At worst case we go through all the nodes, and we check each edge at every node, which turns into O(V+E) time
# Space: At worst case, we need to store all the nodes and all the edges, which is a space complexity of O(V+E)
    def getShortestPath( self, destIndex ):
        path = []
        previousNodeList = self.previousNodeList
        costArray = self.costArray
        currentNode = destIndex

        while currentNode != self.start:
            if previousNodeList[currentNode] == "x":
                return {'cost': float("inf"), 'path': []}

            edgeLength = 0
            for edge in self.network.nodes[previousNodeList[currentNode]].neighbors: # O(1) time, because each node only has 3 neighbors
                if edge.dest.node_id == currentNode:
                    edgeLength = edge.length
                    if edge.length == "x":
                        return {'cost': float("inf"), 'path': []}
            path.append((self.network.nodes[currentNode].loc, self.network.nodes[previousNodeList[currentNode]].loc, '{:.0f}'.format(edgeLength)))
            currentNode = previousNodeList[currentNode]
        return {'cost': costArray[destIndex], 'path': path}


# Time: The complexity changes if we use a MinHeap or an UnSortedArray. For UnSortedArray we get a total complexity of
#       O(V^2+E), for MinHeap, we end up with O((V+E)logV) time complexity, due to the nature of the MinHeap functions
# Space: For both the UnSortedArray and the MinHeap, the space used is O(V) to hold all the nodes and their previous nodes
#       ( as well as distances, but considering we are simply holding two different arrays, O(2V) goes to O(V))
    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.start = srcIndex
        t1 = time.time()

        distanceToNode = {}
        previousNodeList = {}

        for node in self.network.nodes:
            distanceToNode[node.node_id] = float("inf")
            previousNodeList[node.node_id] = "x"
        distanceToNode[srcIndex] = 0

        if use_heap:
            priorityQueue = MinHeap(srcIndex, self.network.nodes)    #O(V) time
        else:
            priorityQueue = UnSortedArray(srcIndex, self.network.nodes)      #O(V) time

        while priorityQueue.getLength() > 0:
            currentNode = priorityQueue.deleteMin()
            #We hit this part of the code at worst V times as we could loop through each node.
            #We end up with a time complexity for deleteMin() * V loops being either O(VlogV) for MinHeap or O(V^2) for the UnSortedArray

            for edge in self.network.nodes[currentNode].neighbors:      # O(1) time, because each node only has 3 neighbors
                if edge.length + distanceToNode[currentNode] < distanceToNode[edge.dest.node_id]:
                    distanceToNode[edge.dest.node_id] = edge.length + distanceToNode[currentNode]
                    previousNodeList[edge.dest.node_id] = currentNode
                    priorityQueue.decreaseKey(edge.dest.node_id, distanceToNode[edge.dest.node_id])
                    #We only hit this part of the code at worst case E times, resulting in a time complexity of O(ElogV) for the
                    #MinHeap and just O(E) for the UnSortedArray
        self.costArray = distanceToNode
        self.previousNodeList = previousNodeList

        #So we get a combined complexity at the end of O(V^2 + E) for the UnSortedArray, and O((V+E)logV) for the MinHeap
        t2 = time.time()
        return (t2-t1)


class UnSortedArray:

# Time: O(V), makeQueue is O(V)
# Space: O(V), same as makeQueue
    def __init__(self, startingNode, allNodes):
        self.makeQueue(startingNode, allNodes)
        return

# Time: O(V), because we just initialize the list of nodes in the network
# Space: O(V), because we store all those values into an array
    def makeQueue(self, startingNode, allNodes):
        self.array = []
        self.length = 0;
        for node in allNodes:   # Runs through for each node V
            self.insert(node.node_id) #O(1) time and space
            self.length += 1
        self.array[startingNode] = 0;


# Time: O(1), its a simple insert
# Space: O(1), inserts a new object into an array of objects.
    def insert(self, node):
        self.array.append(node)
        self.array[node] = float("inf")
        return

# Time: O(1), we don't alter the array
# Space: O(1), we are simply changing a value at an index
    def decreaseKey(self, index, value):
        self.array[index] = value
        return

# Time: O(1)
# Space: O(1)
    def getLength(self):
        return self.length

# Time: Worst case, deleteMin() iterates through each node V, O(V)
# Space: O(1), it just changes the array
    def deleteMin(self):
        index = 0
        min_index = 0
        min = 999999

        for distance in self.array:         # O(V), at most goes through each node
            if distance != "x" and min > self.array[index]:
                min = self.array[index]
                min_index = index
            index += 1

        self.decreaseKey(min_index, "x")
        self.length -= 1
        return min_index

class MinHeap:

# Time: O(VlogV), due to makeQueue
# Space: O(V), due to makeQueue
    def __init__(self, startingNode, allNodes):
        self.makeQueue(startingNode, allNodes)
        return

# Time: O(VlogV), We loop through every node V, each time we insert we also bubble up so that the starting node is the root, which takes logV
#       for a total O(V * logV) which goes to O(VlogV)
# Space: O(V), we keep 3 arrays of size V from this function: O(3V) => O(V)
    def makeQueue(self, startingNode, allNodes):
        self.size = 0
        self.heap = []
        self.heapMap = []
        self.distances = []

        for x in allNodes:
            if x == startingNode:
                self.insert(x, 0)
            else:
                self.insert(x, float("inf"))

# Time: O(logV), simple inserts into the heap and map arrays, then the bubbleUp() gives us the logV
# Space: O(1), just inserting values into an array is constant
    def insert(self, node, startingValue):
        self.heap.append(node.node_id)
        self.distances.append(startingValue)
        self.heapMap.append(node.node_id)
        self.heapMap[node.node_id] = self.size
        self.size += 1
        self.bubbleUp(self.size - 1)
        return

# Time: O(1)
# Space: O(1)
    def getLength(self):
        return self.size

# Time: O(logV), at worst case, we have one node travel all the way up one side of the tree, which results in logV time
# Space: O(1), because we are simply swapping values, but no other array is created
    def bubbleUp(self, index):
        parentGreater = True
        while index != 0 and parentGreater:
            childNode = self.heap[index]
            parentIndex = self.parentIndex(index)
            parentNode = self.heap[parentIndex]
            childDistance = self.distances[self.heap[index]]
            parentDistance = self.distances[self.heap[self.parentIndex(index)]]
            if childDistance < parentDistance:

                self.heap[index] = parentNode
                self.heap[parentIndex] = childNode

                self.heapMap[childNode] = parentIndex
                self.heapMap[parentNode] = index
            else:
                parentGreater = False

            index = self.parentIndex(index)

        return

# Time: O(logV), the only time complexity here comes from the call to bubbleUp(), which is logV time worst case
# Space: O(1), only alteration at a index is done here, even bubbleUp() is O(1) space
    def decreaseKey(self, index, value):
        self.distances[index] = value
        self.bubbleUp(self.heapMap[index])
        return

# Time: O(logV) at worst case. Because we swap the first index to the last before deleting, the python del function is O(1).
#       There are other cases of simply altering an index before we trickle down, which is where the majority of our time
#       complexity comes from. This part is O(logV) because at worst case we take the top node and trickle it all the way down
#       one side of the tree to the end, resulting in a time complexity of O(logV)
# Space: O(1), everything we do in this function consists of updating indices and swapping indicies.
    def deleteMin(self):
        nodeToReturn = self.heap[0]     #Swaps and updating indices are constant time and space
        self.heap[0] = self.heap[-1]
        self.heap[-1] = nodeToReturn

        self.heapMap[self.heap[0]] = 0
        self.heapMap[nodeToReturn] = "x"

        del self.heap[-1]

        currentIndex = 0
        while currentIndex*2 + 2 < self.size -1:            #This at worst case is O(logV) time
            minChildIndex = self.childMin(currentIndex)

            if self.distances[self.heap[minChildIndex]] < self.distances[self.heap[currentIndex]]:
                childNode = self.heap[minChildIndex]        #All these swaps are constant time and space
                parentNode = self.heap[currentIndex]
                self.heap[currentIndex] = childNode
                self.heap[minChildIndex] = parentNode

                childNodeMap = self.heapMap[childNode]
                parentNodeMap = self.heapMap[parentNode]
                self.heapMap[childNode] = parentNodeMap
                self.heapMap[parentNode] = childNodeMap

            currentIndex = minChildIndex
        self.size -= 1
        return nodeToReturn

# Time: O(1), simple calculations
# Space: O(1), simply returns a number
    def parentIndex(self, index):
        return (index - 1)//2

# Time: O(1), simple calculations and comparisions
# Space: O(1), returns a single number, other intializations are constant space
    def childMin(self, parentIndex):
        rightChildIndex = parentIndex*2 + 2
        leftChildIndex = parentIndex*2 + 1

        if self.distances[self.heap[rightChildIndex]] > self.distances[self.heap[leftChildIndex]]:
            min = leftChildIndex
        else:
            min = rightChildIndex
        return min
