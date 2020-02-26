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

        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL
        #       NEED TO USE

            # path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
        path = [];
        previousNodeList = self.prev
        costList = self.cost
        currentNode = destIndex

        while currentNode != self.source:
            if previousNodeList[currentNode] == "x":
                return {'cost': float("inf"), 'path': []}

            edgeLength = 0
            for edge in self.network.nodes[currentNode].neighbors:
                if edge.dest.node_id == previousNodeList[currentNode]:
                    edgeLength = edge.length
                    if edge.length == "x":
                        return {'cost': float("inf"), 'path': []}
            path.append((self.network.nodes[currentNode].loc, self.network.nodes[currentNode].loc, '{:.0f}'.format(edgeLength)))
            currentNode = previousNodeList[currentNode]

        return {'cost': costList[destIndex], 'path': path}




    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()

        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        dist = {}
        prev = {}

        for node in self.network.nodes:
            dist[node.node_id] = float("inf")
            prev[node.node_id] = "x"

        if use_heap:
            print("want to use the heap!")
        else:
            queue = UnSortedArray(srcIndex, self.network.nodes)

        while queue.getLength() > 0:

            currentNode = queue.deleteMin()
            for edge in self.network.nodes[currentNode].neighbors:
                if edge.length + dist[currentNode] < dist[edge.dest.node_id]:
                    dist[edge.dest.node_id] = edge.length + dist[currentNode]
                    prev[edge.dest.node_id] = currentNode
                    queue.decreaseKey(edge.dest.node_id, dist[edge.dest.node_id])

        self.cost = dist
        self.prev = prev

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

    def decreaseKey(self, node, value):
        self.array[node] = value
        return

    def getLength(self):
        return self.length

    def deleteMin(self):
        index = 0
        min_index = 0

        for x in self.array:
            if x != "x":
                min = x
                break

        for distance in self.array:
            if distance != "x" and min > self.array[index]:
                min_index = index
            index += 1

        self.array[min_index] = "x"
        self.length -= 1
        return min_index
