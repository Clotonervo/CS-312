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
	def greedy( self,time_allowance=60.0 ):

		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		bssf = None
		bssfCost = np.inf
		count = 0
		start_time = time.time()

		for startCity in cities:			# O(n), loops through each city once
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
		
	def branchAndBound( self, time_allowance=60.0 ):
		foundTour = False;
		greedyResults = self.greedy(1000)
		bssf = greedyResults['soln']
		bssfCost = greedyResults['cost']
		count = 0
		results = {}
		cities = self._scenario.getCities()
		queue = []

		startingReducedCostMatrix, lowerBound = self.initReducedCostMatrix(cities)
		start_time = time.time()

		# cost, current matrix, current city, list of all other cities,
		startingCity = {'cost':lowerBound, 'matrix':startingReducedCostMatrix, 'current':cities[0], 'cityList':cities[1:], 'route':[cities[0]]}		#FIXME: Figure out if using a dict messes with the heap
		heapq.heappush(queue, startingCity)

		while time.time()-start_time < time_allowance and (len(queue) > 0):
			#Figure out how to choose which one to do next
			currentSubProblem = heapq.heappop(queue)
			if currentSubProblem['cost'] < bssfCost:
				currentCity = currentSubProblem['current']
				for city in currentSubProblem['cityList']:
					if city.costTo()


		pass


	def initReducedCostMatrix(self, cities):
		matrix = [[0 for i in range(len(cities))] for j in range(len(cities))]

		for i in range(len(cities)):
			for j in range(len(cities)):
				if i == j:
					matrix[i][j] = np.inf
				else:
					matrix[i][j] = cities[i].costTo(cities[j])

		rowMins = np.min(matrix, 1)
		lowerBound = 0

		for i in range(len(cities)):			# Row reductions
			lowerBound += rowMins[i]
			for j in range(len(cities)):
				matrix[i][j] -= rowMins[i]

		colMins = np.min(matrix, 0)

		for i in range(len(cities)):			# Column reductions
			lowerBound += colMins[i]
			for j in range(len(cities)):
				matrix[i][j] -= colMins[j]

		return matrix, lowerBound


	def reducedCostMatrix(self, currentInfo):
		# Make deep copies of things
		# Impliment this




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
		



