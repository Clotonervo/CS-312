#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__( self ):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex

        path = []
        previousNodeList = self.prev
        costList = self.cost
        currentNode = destIndex

        while currentNode != self.start:
            if previousNodeList[currentNode] == "x":
                return {'cost': 9999999999, 'path': []}

            edgeLength = 0
            for edge in self.network.nodes[previousNodeList[currentNode]].neighbors:
                if edge.dest.node_id == currentNode:
                    edgeLength = edge.length
                    if edge.length == "x":
                        return {'cost': 99999999999, 'path': []}
            path.append((self.network.nodes[currentNode].loc, self.network.nodes[previousNodeList[currentNode]].loc, '{:.0f}'.format(edgeLength)))
            currentNode = previousNodeList[currentNode]
        return {'cost': costList[destIndex], 'path': path}




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
            queue = MinHeap(srcIndex, self.network.nodes)
        else:
            queue = UnSortedArray(srcIndex, self.network.nodes)

        while queue.getLength() > 0:
            currentNode = queue.deleteMin()

            for edge in self.network.nodes[currentNode].neighbors:
                if edge.length + distanceToNode[currentNode] < distanceToNode[edge.dest.node_id]:
                    distanceToNode[edge.dest.node_id] = edge.length + distanceToNode[currentNode]
                    previousNodeList[edge.dest.node_id] = currentNode
                    queue.decreaseKey(edge.dest.node_id, distanceToNode[edge.dest.node_id])
        self.cost = distanceToNode
        self.prev = previousNodeList

        t2 = time.time()
        return (t2-t1)


class UnSortedArray:
    def __init__(self, startingNode, allNodes):
        self.array = []
        self.length = 0;
        for node in allNodes:
            self.insert(node.node_id)
            self.length += 1
        self.array[startingNode] = 0;


    def insert(self, node):
        self.array.append(node)
        self.array[node] = float("inf")
        return

    def decreaseKey(self, index, value):
        self.array[index] = value
        return

    def getLength(self):
        return self.length

    def deleteMin(self):
        index = 0
        min_index = 0
        min = 999999

        for distance in self.array:
            if distance != "x" and min > self.array[index]:
                min = self.array[index]
                min_index = index
            index += 1

        self.array[min_index] = "x"
        self.length -= 1
        return min_index

class MinHeap:
    def __init__(self, startingNode, allNodes):
        self.size = 0
        self.heap = []
        self.heapMap = []
        self.distances = []

        for x in allNodes:
            if x.node_id == startingNode:
                self.insert(x, 0)
            else:
                self.insert(x,float("inf"))

        return

    def getLength(self):
        return self.size

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

    def insert(self, node, startingValue):
        self.heap.append(node.node_id)
        self.distances.append(startingValue)
        self.heapMap.append(node.node_id)
        self.heapMap[node.node_id] = self.size
        self.size += 1
        self.bubbleUp(self.size - 1)
        return

    def decreaseKey(self, index, value):
        # Change the value and then rearrange it on the heap
        self.distances[index] = value
        self.bubbleUp(self.heapMap[index])
        return

    def deleteMin(self):

        nodeToReturn = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap[-1] = nodeToReturn

        self.heapMap[self.heap[0]] = 0
        self.heapMap[nodeToReturn] = "x"

        del self.heap[-1]

        currentIndex = 0
        while currentIndex*2 + 2 < self.size -1:
            minChildIndex = self.childMin(currentIndex)

            if self.distances[self.heap[minChildIndex]] < self.distances[self.heap[currentIndex]]:
                childNode = self.heap[minChildIndex]
                parentNode = self.heap[currentIndex]
                self.heap[currentIndex] = childNode
                self.heap[minChildIndex] = parentNode

                childNodeMap = self.heapMap[childNode]
                parentNodeMap = self.heapMap[parentNode]
                self.heapMap[childNode] = parentNodeMap
                self.heapMap[parentNode] = childNodeMap

            currentIndex = minChildIndex


        # See if here we trickle down once we change the minimum
        self.size -= 1
        return nodeToReturn

    def parentIndex(self, index):
        return (index - 1)//2

    def childMin(self, parentIndex):
        rightChildIndex = parentIndex*2 + 2
        leftChildIndex = parentIndex*2 + 1

        if self.distances[self.heap[rightChildIndex]] > self.distances[self.heap[leftChildIndex]]:
            min = leftChildIndex
        else:
            min = rightChildIndex
        return min
