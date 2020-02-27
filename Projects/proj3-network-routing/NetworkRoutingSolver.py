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

        print("previousNodeList = ", previousNodeList)
        print("costList = ", costList);

        while currentNode != self.source:
            if previousNodeList[currentNode] == "x":
                return {'cost': float("inf"), 'path': []}

            edgeLength = 0
            print("currentNode: ", currentNode)
            print("Neighbors: ", self.network.nodes[currentNode].neighbors)
            print("PreviousNode: ", previousNodeList[currentNode])
            for edge in self.network.nodes[currentNode].neighbors:
                if edge.dest.node_id == previousNodeList[currentNode]:
                    print("Edge found! Length: ", edge.length)
                    edgeLength = edge.length
                    if edge.length == "x":
                        return {'cost': float("inf"), 'path': []}
            path.append((self.network.nodes[currentNode].loc, self.network.nodes[previousNodeList[currentNode]].loc, '{:.0f}'.format(edgeLength)))
            currentNode = previousNodeList[currentNode]
        print(costList[destIndex])
        return {'cost': costList[destIndex], 'path': path}




    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
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

        print(distanceToNode)

        # if use_heap:
        #     print("want to use the heap!")
        # else:
        queue = UnSortedArray(srcIndex, self.network.nodes)

        while queue.getLength() > 0:
            currentNode = queue.deleteMin()
            print("currentNode", currentNode)
            for edge in self.network.nodes[currentNode].neighbors:
                print(edge)
                print(distanceToNode[edge.dest.node_id])
                if edge.length + distanceToNode[currentNode] < distanceToNode[edge.dest.node_id]:
                    print("edge found smaller = ", edge)
                    distanceToNode[edge.dest.node_id] = edge.length + distanceToNode[currentNode]
                    previousNodeList[edge.dest.node_id] = currentNode
                    queue.decreaseKey(edge.dest.node_id, distanceToNode[edge.dest.node_id])
            print("previousNode List =====", previousNodeList)

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
                min_index = index
            index += 1

        self.array[min_index] = "x"
        self.length -= 1
        return min_index
