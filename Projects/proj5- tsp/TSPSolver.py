#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
import copy



class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	# Time: O(n^3), we loop through each city starting with a new one each time, then we loop through each city in
	#		and see if we can get to it from the current city, and we do that until we reach all the cities, which leaves
	# 		us looping n^3 times
	# Space: O(n), each outer loop we store an array of cities that signify the routes of size n, but because we reuse this
	#		variable, our space complexity is only O(n)
	def greedy(self, time_allowance=60.0):

		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		bssf = None
		bssfCost = np.inf
		count = 0
		start_time = time.time()

		for startCity in cities:			# O(n), loops through each city once, changing the start city each time
			currentRoute = [startCity]
			currentCity = startCity

			while len(currentRoute) < ncities:	# O(n) loops through up to n times, with currentCity being updated
				nextDistance = np.inf
				nextCity = None
				for cityOption in cities:				# O(n) loops though each city in row and finds the next city to travel to
					if not (cityOption in currentRoute):
						if currentCity.costTo(cityOption) < nextDistance:
							nextDistance = currentCity.costTo(cityOption)
							nextCity = cityOption

				if nextDistance == np.inf:
					break
				else:
					currentCity = nextCity
					currentRoute.append(nextCity)

			if len(currentRoute) == ncities:					# Solution found!
				solutionReference = TSPSolution(currentRoute)
				if solutionReference.cost < bssfCost:			# Check to see if its the best solution
					bssfCost = solutionReference.cost
					bssf = solutionReference
					count += 1

		end_time = time.time()
		results['cost'] = bssfCost
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None

		return results





	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''
# Time: O(n^3*(n-1)!), due to each subproblem expanding in O(n^3) time, up to
#		(n-1)! times for each possible subproblem
# Space: O(n^2*(n-1)!), enough space to hold a 2d matrix in the queue, up to
#		(n-1)! times for each possible subproblem
	def branchAndBound(self, time_allowance=60.0):
		greedyResults = self.greedy(time_allowance)
		bssf = greedyResults['soln']
		bssfCost = greedyResults['cost']
		count = 0
		results = {}
		cities = self._scenario.getCities()
		queue = []
		pruned = 0
		totalNodes = 0
		maxNumberStates = 0
		startingReducedCostMatrix, lowerBound = self.initReducedCostMatrix(cities)	# O(n^2)

		# Tuple of cost, current matrix, current city, list of all other cities, and route
		startingCity = (-1 ,lowerBound, cities[0], startingReducedCostMatrix, cities[1:], [cities[0]])
		heapq.heappush(queue, startingCity)
		totalNodes += 1

		start_time = time.time()

		while time.time()-start_time < time_allowance and (len(queue) > 0):		# O((n-1)!) time complexity!
			# O(logn) pop time, this gets swallowed up by other complexities
			currentSubProblem = heapq.heappop(queue)	# Subproblems are popped based on cost (maybe should change this)
			curCost = currentSubProblem[1]
			currentCity = currentSubProblem[2]
			curMatrix = currentSubProblem[3]
			curRoute = currentSubProblem[5]
			curDestinations = currentSubProblem[4]
			if curCost < bssfCost:						# Check the current cost to see if we need to prune
				for city in curDestinations:			# For each city, expand the sub problem if an edge exists
					if currentCity.costTo(city) < np.inf and (city not in curRoute):
						# Edge exists, get reduced cost matrix and other node data, O(n^2) space and time complexity
						if(curCost + curMatrix[currentCity._index][city._index]) > bssfCost: # Quick pruning possibly
							totalNodes += 1
							pruned += 1
							continue

						newSubProblem = self.createSubproblem(currentCity, city, curCost, curMatrix, curRoute, curDestinations)
						totalNodes += 1
						newDestinationList = newSubProblem[4]
						newCost = newSubProblem[1]
						newRoute = newSubProblem[5]

						if len(newDestinationList) > 0:
							if newCost > bssfCost:	# Is our new node worth our time?
								pruned += 1				# Nope! Prune it
							else:
								# O(logn) push time, also gets swallowed up by bigger complexities
								heapq.heappush(queue, newSubProblem) 	# Add the node to the queue to expand later
						else:
							solutionReference = TSPSolution(newRoute)	# We found a solution!
							if bssfCost > solutionReference.cost:		# Check to see if we update our BSSF
								bssfCost = solutionReference.cost
								bssf = solutionReference
								count += 1
							else:
								pruned += 1

				currentQueueSize = len(queue)		# After each sub problem expansion, check the queue size and keep the max
				if currentQueueSize > maxNumberStates:
					maxNumberStates = currentQueueSize
			else:
				pruned += 1		# Cost of current sub problem is greater than BSSF cost, prune it

		end_time = time.time()
		pruned += len(queue)
		results['cost'] = bssfCost
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = maxNumberStates
		results['total'] = totalNodes
		results['pruned'] = pruned

		return results


	# Time: O(n^2), due to matrix intialization, and a lot of updating to every element in the 2d matrix
	# Space: O(n^2), enough space to hold a 2d matrix
	def initReducedCostMatrix(self, cities):
		matrix = [[0 for i in range(len(cities))] for j in range(len(cities))]		# O(n^2) time and space initializing matrix

		for i in range(len(cities)):			# O(n^2), as it loops through each element in 2d matrix
			for j in range(len(cities)):
				if i == j:
					matrix[i][j] = np.inf
				else:
					matrix[i][j] = cities[i].costTo(cities[j])

		rowMins = np.min(matrix, 1)
		lowerBound = 0

		for i in range(len(cities)):			# Row reductions, also O(n^2)
			lowerBound += rowMins[i]
			for j in range(len(cities)):
				matrix[i][j] -= rowMins[i]

		colMins = np.min(matrix, 0)

		for i in range(len(cities)):			# Column reductions, also O(n^2)
			lowerBound += colMins[i]
			for j in range(len(cities)):
				matrix[i][j] -= colMins[j]

		return matrix, lowerBound

	# Time: O(n^2), We iterate through each element in the 2d matrix multiple times
	# Space: O(n^2), enough space to hold a copy of a 2d matrix
	def createSubproblem(self, currentCity, destination, parentCost, parentMatrix, parentRoute, cityList):
		# Make deep copies of things
		matrix = copy.deepcopy(parentMatrix)
		cost = parentCost
		route = copy.deepcopy(parentRoute)
		newCityList = copy.deepcopy(cityList)

		cost += matrix[currentCity._index][destination._index]

		for i in range(len(matrix[currentCity._index])):		# Create the reduced cost matrix, O(n^2)
			matrix[currentCity._index][i] = np.inf

		for i in range(len(matrix)):
			matrix[i][destination._index] = np.inf

		rowMins = np.min(matrix, 1)
		reductionCost = 0

		for i in range(len(matrix)):  # Row reductions, O(n^2)
			if rowMins[i] == np.inf:
				continue
			reductionCost += rowMins[i]
			for j in range(len(matrix[i])):
				matrix[i][j] -= rowMins[i]

		colMins = np.min(matrix, 0)

		for i in range(len(matrix)):  # Column reductions, O(n^2
			if colMins[i] < np.inf:
				reductionCost += colMins[i]
			for j in range(len(matrix[i])):
				if colMins[j] == np.inf:
					continue
				matrix[i][j] -= colMins[j]

		cost += reductionCost			# O(1) operations
		route.append(destination)
		destinationIndex = cityList.index(destination)
		del newCityList[destinationIndex]


		newSubProblem = (len(route) * -1, cost, destination, matrix, newCityList, route)			# New sub problem information
		return newSubProblem



	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy( self,time_allowance=60.0 ):
		pass
