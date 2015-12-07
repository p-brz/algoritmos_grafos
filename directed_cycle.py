#!/usr/bin/env python

import graphs
from graphs import Dfs

class DirectedCycleDetector(object):
	def __init__(self, graph):
		self.graph = graph
		self.reset()

	def reset(self):
		self.resetCycle()
		self.inVisit = []

	def resetCycle(self):
		self.cycle = []

	def checkCycle(self):
		self.reset()

		iterator = Dfs(self.graph)
		for i in range(self.graph.count()):
			if not iterator.hasVisited(i):
				iterator.visit(i, self)
				if self.hasCycle():
					return True
		return False

	def onVisit(self, vertice):
		if self.hasCycle():
			return

		self.inVisit.append(vertice)

		for v in self.graph.adjacents(vertice):
			if v in self.inVisit:
				self._onCycleDetection(v)
				return

	def onFinishVisit(self, vertice):
		if not self.hasCycle():
			self.inVisit.remove(vertice)

	def _onCycleDetection(self, vertice):
		idx = self.inVisit.index(vertice)
		cycle = []
		for i in range(idx, len(self.inVisit)):
			cycle.append(self.inVisit[i])
		cycle.append(vertice)

		self.cycle = cycle

	def hasCycle(self):
		return len(self.cycle) > 0

	def getCycle(self):
		return self.cycle

import sys

def main():
	if len(sys.argv) <= 1:
		return

	g = graphs.readDirected(sys.argv[1])
	cycleDetect = DirectedCycleDetector(g)
	cycleDetect.checkCycle()

	print "Graph has cycle? %s" % cycleDetect.hasCycle()
	print "Graph cycle: %s" % cycleDetect.getCycle()

	print g

if __name__=="__main__":
	main()
