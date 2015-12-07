import graphs


class MSTBuilder(object):
	def __init__(self, graph):
		self.graph = graph
		self.edges = []
	def getEdges(self):
		if(not self.edges):
			self.edges = self.buildMST()

		return self.edges

	def buildMST(self):
		return []

class PrimMSTBuilder(MSTBuilder):
	def buildMST(self):
		numV = self.graph.count()
		self.connected		= [False] * numV
		self.edgeConnection = {}
		self.edges = []

		self.putVertice(0)
		minE = self.getMinEdge()

		while len(self.edges) < numV - 1 and minE:
			if(not self.isConnected(minE[0])):
				self.putVertice(minE[0])
				self.edges.append(minE)
			elif not self.isConnected(minE[1]):
				self.putVertice(minE[1])
				self.edges.append(minE)

			minE = self.getMinEdge()

		return self.edges

	def putVertice(self, vertice):
		self.connected[vertice] = True

		for e in self.graph.getEdges(vertice):
			otherV = e.other(vertice)
			if not self.isConnected(otherV):
				otherE = self.edgeConnection.get(otherV, None)
				if(not otherE or otherE.getWeight() > e.getWeight()):
					self.edgeConnection[otherV] = e

	def getMinEdge(self):
		minEdge = None
		minV = None
		for v in self.edgeConnection:
			e = self.edgeConnection[v]
			if not minEdge or minEdge.getWeight() > e.getWeight():
				minEdge = e
				minV = v

		if(minEdge and minV):
			del self.edgeConnection[minV]

		return minEdge

	def isConnected(self, v):
		return self.connected[v]

import sys

def main():
	if len(sys.argv) <= 1:
		return

	g = graphs.readWeighted(sys.argv[1])
	mst = PrimMSTBuilder(g)

	print g

	print "Minimum Spanning Tree:"
	for e in mst.getEdges():
		print e

if __name__=="__main__":
	main()
