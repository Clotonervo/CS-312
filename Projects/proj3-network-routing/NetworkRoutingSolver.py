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

        path = [];
        previousNodeList = self.prev
        costList = self.cost
        currentNode = destIndex

        while currentNode != self.start:
            if previousNodeList[currentNode] == "x":
                return {'cost': 9999999999, 'path': []}

            edgeLength = 0
            for edge in self.network.nodes[previousNodeList[currentNode]].neighbors:
                if edge.dest.node_id == currentNode:
                    # print("Edge found! Length: ", edge.length)
                    edgeLength = edge.length
                    if edge.length == "x":
                        return {'cost': 99999999999, 'path': []}
            path.append((self.network.nodes[currentNode].loc, self.network.nodes[previousNodeList[currentNode]].loc, '{:.0f}'.format(edgeLength)))
            currentNode = previousNodeList[currentNode]
        return {'cost': costList[destIndex], 'path': path}




    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.start = srcIndex
        t1 = time.time()

        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        distanceToNode = {}
        previousNodeList = {}

        for node in self.network.nodes:
            distanceToNode[node.node_id] = float("inf")
            previousNodeList[node.node_id] = "x"
        distanceToNode[srcIndex] = 0;

        if use_heap:
            queue = MinHeap(srcIndex, self.network.nodes)
        else:
            queue = UnSortedArray(srcIndex, self.network.nodes)

        print("Queue heap: ", queue.heap)
        print("Queue distances: ", queue.distances)
        print("Queue Map: ", queue.heapMap)
        print("Starting Node: ", srcIndex)

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
        print("-------------------")
        while index != 0:
            print("index = ", index)
            print("child number: ", self.distances[index])
            print("parent number: ", self.distances[self.parentIndex(index)])
            if self.distances[index] < self.distances[self.parentIndex(index)]:
                #swap them
                # print(self.heap)
                tempMinDistance = self.distances[self.parentIndex(index)]
                self.distances[self.parentIndex(index)] = self.distances[index]
                self.distances[index] = tempMinDistance

                parentNode = self.heap[self.parentIndex(index)]
                self.heap[self.parentIndex(index)] = self.heap[index]
                self.heap[index] = parentNode

                newParentLocation = self.parentIndex(index)
                self.heapMap[self.heap[index]] = index
                self.heapMap[self.heap[self.parentIndex(index)]] = self.parentIndex(index)
                print(self.heap)
                print(self.heapMap)
                print(self.distances)
            index = index//2

        return

    def insert(self, node, startingValue):
        print("adding: ", node)
        print("-- - - - - - - - - --")
        self.heap.append(node.node_id)
        self.distances.append(startingValue)
        self.heapMap.append(node.node_id)
        self.heapMap[node.node_id] = self.size
        self.size += 1
        self.bubbleUp(self.size - 1)
        return

    def decreaseKey(self, index, value):
        # Change the value and then rearrange it on the heap
        return

    def deleteMin(self):
        self.size -= 1
        # See if here we trickle down once we change the minimum
        return

    def parentIndex(self, index):
        return (index - 1)//2
