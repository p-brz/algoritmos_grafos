#!/usr/bin/env python

class Graph(object):
	def __init__(self, numVertices=0):
		self.adjs = []
		for i in range(numVertices):
			self.addVertice()

	def addVertice(self):
		self.adjs.append(set())
		return self.count() - 1

	def addEdge(self, u, v):
		self.adjs[u].add(v)
		self.adjs[v].add(u)

	def removeEdge(self, u, v):
		self.adjs[u].remove(v)
		self.adjs[v].remove(u)

	def hasEdge(self, u, v):
		return v in self.adjacents(u);

	def adjacents(self, v):
		return self.adjs[v]

	def count(self):
		return len(self.adjs)

	def __str__(self):
		out = ""
		for v in range(self.count()):
			out += "%d : %s\n" % (v, str(list(self.adjacents(v))))

		return out

class DirectedGraph(Graph):
	def __init__(self, numVertices=0):
		super(DirectedGraph, self).__init__(numVertices)

	def addEdge(self, u, v):
		self.adjs[u].add(v)

	def removeEdge(self, u, v):
		self.adjs[u].remove(v)

class Edge(object):
	def __init__(self, v, u, weight=1):
		self.v1 = v
		self.v2 = u
		self.weight = weight

	def getV1(self):
		return self.v1
	def getV2(self):
		return self.v2
	def getWeight(self):
		return self.weight
	def other(self, v):
		return self.getV1() if v == self.getV2() else self.getV2()
	def __float__(self):
		return self.getWeight()
	def __cmp__(self, other):
		if(self.getWeight() < float(other)):
			return -1
		elif(self.getWeight() > float(other)):
			return 1
		else:
			return 0
	def __eq__(self, other):
		return other.getV1() == self.getV1()  \
				and other.getV2() == self.getV2() \
				and other.getWeight() == self.getWeight()
	def __getitem__(self, k):
		if(k == 0):
			return self.getV1()
		elif(k == 1):
			return self.getV2()
		elif(k == 2):
			return self.getWeight()

		raise IndexError()

	def __str__(self):
		return "%d-%d(%0.2f)" % (self.v1, self.v2, self.getWeight())
	def __repr__(self):
		return self.__str__()

class WeightedGraph(Graph):
	def _super(self):
		return super(WeightedGraph, self)

	def __init__(self, numVertices=0):
		self.edges = []
		self._super().__init__(numVertices)

	def addVertice(self):
		self._super().addVertice()
		self.edges.append(set())

	def addEdge(self, u, v, weight=1):
		self._super().addEdge(u, v)
		e = Edge(u, v, weight)
		self.edges[u].add(e)
		self.edges[v].add(e)

	def getEdges(self, v):
		return self.edges[v]

	def __str__(self):
		out = ""
		for v in range(self.count()):
			edgesStr = [ "%d(%0.2f)" % (e.other(v), e.getWeight()) \
												for e in self.getEdges(v)]
			out += "%d : %s\n" % (v, edgesStr)

		return out
	def __repr__(self):
		return self.__str__()

class Dfs(object):
	def __init__(self, graph):
		self.graph = graph
		self.reset()

	def fullVisit(self, visitor=None):
		for i in range(self.graph.count()):
			if not self.hasVisited(i):
				self.visit(i, visitor)

	def visit(self, source=0, visitor=None):
		self._visit(source, visitor)

	def reset(self):
		self.visited = [False] * self.graph.count()

	def _visit(self, vert, visitor):
		self.visited[vert] = True

		if(visitor):
			visitor.onVisit(vert)

		for v in self.graph.adjacents(vert):
			if not self.hasVisited(v):
				self._visit(v, visitor)

		if(visitor):
			visitor.onFinishVisit(vert)

	def hasVisited(self, vert):
		return self.visited[vert]

class GraphReader(object):
	def readGraph(self, filepath):
		gFile = open(filepath, 'r')

		numVertices = int(gFile.readline())
		edges = []

		for line in gFile.readlines():
			e = line.split()
			edges.append(e)

		return self.makeGraph(numVertices, edges)

	def makeGraph(self, numVertices, edges):
		graph = self._createGraph(numVertices)
		for e in edges:
			self._addEdge(graph, e)

		return graph

	def _createGraph(self, numVertices):
		return Graph(numVertices)

	def _addEdge(self, graph, edge):
		graph.addEdge(int(edge[0]), int(edge[1]))


class DirectedGraphReader(GraphReader):
	def _createGraph(self, numVertices):
		return DirectedGraph(numVertices)

class WeightedGraphReader(GraphReader):
	def _createGraph(self, numVertices):
		return WeightedGraph(numVertices)

	def _addEdge(self, graph, edge):
		graph.addEdge(int(edge[0]), int(edge[1]), float(edge[2]))


def readDirected(filepath):
	return DirectedGraphReader().readGraph(filepath)

def readWeighted(filepath):
	return WeightedGraphReader().readGraph(filepath)

def reverse(graph):
	rGraph = DirectedGraph(graph.count())

	for v in range(graph.count()):
		for u in graph.adjacents(v):
			rGraph.addEdge(u, v)

	return rGraph
