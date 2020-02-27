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

        # if use_heap:
        #     print("want to use the heap!")
        # else:
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
        min = 99999

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
        return

    def getLength(self):
        return self.size

    def insert(self, node):
        return

    def decreaseKey(self, index, value):
        return

    def deleteMin(self):
        return
