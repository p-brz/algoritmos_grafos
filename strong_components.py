import graphs
import directed_cycle
from topological_sort import TopologicalSort

# Algoritmo de Kosaraju
class StrongComponentsFinder(object):
	def __init__(self, graph):
		self.graph = graph
		self.reset()

	def reset(self):
		self.id = range(self.graph.count())
		self.compCount = 0

	def findComponents(self):
		reversedGraph = graphs.reverse(self.graph)
		topolOrder = TopologicalSort(reversedGraph, True).sort()

		print "graph: %s" % self.graph
		print "reverse graph: %s" % reversedGraph
		print "reverse post order: %s" % topolOrder


		iterator = graphs.Dfs(self.graph)
		for v in topolOrder:
			if(not iterator.hasVisited(v)):
				print "visit from %d" % v
				iterator.visit(v, self)
				self.compCount+=1

		print self.id

		return self._getComponents()

	def onVisit(self, vertice):
		print "visit %d" %vertice
		self.id[vertice] = self.compCount

	def onFinishVisit(self, vertice):
		print "finish visit %d" %vertice

	def _getComponents(self):
		compDict = {}
		for i in range(self.graph.count()):
			id = self.id[i]

			if(not id in compDict):
				compDict[id] = []
			compDict[id].append(i)

		components = []
		for key in compDict:
			components.append(compDict[key])

		return components

import sys

def main():
	if len(sys.argv) <= 1:
		return

	g = graphs.readDirected(sys.argv[1])
	compFinder = StrongComponentsFinder(g)
	components = compFinder.findComponents()

	print "Found %d components" % len(components)
	print components


if __name__=="__main__":
	main()
