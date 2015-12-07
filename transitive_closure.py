import graphs

class ReachableBuilder(object):
	def __init__(self, graph, vertice):
		self.reachables = set()
		iterator = graphs.Dfs(graph)
		iterator.visit(vertice, self)

	def getReachables(self):
		return self.reachables

	def onVisit(self, v):
		self.reachables.add(v)

	def onFinishVisit(self, v):
		pass

class ReachabilityFinder(object):
	def __init__(self, graph):
		self.reachabilityMatrix = [None] * graph.count()
		self.graph = graph

	def findReachables(self):
		for v in range(self.graph.count()):
			r = ReachableBuilder(self.graph, v)
			self.reachabilityMatrix[v] = r.getReachables()

	def reachables(self, vertice):
		return self.reachabilityMatrix[vertice]

	def reachable(self, fromVertice, toVertice):
		R = self.reachabilityMatrix
		return R[fromVertice] and toVertice in R[fromVertice]

import sys

def main():
	if len(sys.argv) <= 1:
		return

	g = graphs.readDirected(sys.argv[1])
	r = ReachabilityFinder(g)
	r.findReachables()

	for v in range(g.count()):
		print "%d reachability: %s" % (v, r.reachables(v))


if __name__=="__main__":
	main()
