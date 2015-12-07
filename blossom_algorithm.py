#! /usr/bin/env python

import graphs
from graphs import *
import sys


class BlossomMatching(object):
	def __init__(self, graph):
		self.g = graph
		self.matching = Graph(graph.count())

	def findMaximumMatching(self):
		#While is possible, augment the matching
		while(self.augmentMatching()):
			pass
		return self.matching

	def augmentMatching(self):
		#Find an alternating path
		p = self.findAugmentPath(self.g, self.matching)
		if(len(p) > 0):
			#Increase the match with this path
			self.increaseMatching(p)
			return True

		return False

	def findAugmentPath(self, graph, matching):
		return AugmentPathFinder(graph, matching).findPath();

	def increaseMatching(self, path):
		print "increase matching by: ", path

		# For each edge on the path
		for i in range(len(path) - 1):
			v1 = path[i]
			v2 = path[i + 1]

			self.revertEdge(v1, v2)

		print "now matching is: \n", self.matching

	def revertEdge(self, v1, v2):
		if(self.matching.hasEdge(v1, v2)):
			self.matching.removeEdge(v1, v2)
		else:
			self.matching.addEdge(v1, v2)

class AugmentPathFinder(object):
	def __init__(self, graph, matching):
		self.graph = graph
		self.matching = matching
		self.edgeQueue = []

	def findPath(self):
		forest = Forest()

		self.initForestWithExposedVertices(forest)

		# While there is edges to handle
		while(len(self.edgeQueue) > 0):
			edge = self.edgeQueue.pop(0)

			path = self.processEdge(forest, edge);

			# If found a path
			if(path is not None):
				# Return that path
				return path

		#There is no augmenting path
		return []

	def initForestWithExposedVertices(self, forest):
		#for each exposed vertice
		for v in self.getExposedVertices():
			#create  an empty tree on forest
			forest.addTree(v)
			#queue the edges from that vertice
			self.queueEdges(v)

	''' Analyzes a given edge, relative to the forest, and try to find a path from it'''
	def processEdge(self, forest, edge):
		#src vertice is on forest, because only edges relative to vertices on
		#forest are enqueued to be processed
		src = edge.getV1()
		dst = edge.getV2()

		#If the dst vertice is not on the forest
		if(not forest.hasVert(dst)):
			#then it is a matched vertice (all unmatched vertices were added previously on initialization)
			#so, add it and his matched vertice to the forest (ensure an alternating path)
			self.addMatchedVert(dst, src, forest)
		elif forest.isOuterNode(dst):
			'''Outer nodes are on a even distance from the tree root (the exposed vertice),
				so they can make an alternating path.
				Because 'inner nodes' cannot make algumenting path, we ignore them.
			'''
			if forest.verticesAreOnSameTree(src, dst):
				# Found a blossom!
				# These vertices has a common root (are on same tree), but a diferent path to it.
				# so, a connection between them (the edge) forms a cycle.
				# Because both are 'outer nodes', the cycle is alternating and a blossom
				blossom = Blossom.makeBlossom(forest, src, dst)

				# Try find the path using the contracted graph
				return self.findPathByContracting(blossom)
			else:
				# Vertices are not on same tree, so found an augmenting path
				# that connects the root of the first tree to the root of second
				# tree (two exposed vertices)
				return self.makeAugmentPath(forest, src, dst)
		return None

	def findPathByContracting(self, blossom):
		return ContractedAugmentPathFinder(self.graph, self.matching, blossom).findPath()

	# return all vertices that are not on the match (exposed vertices)
	def getExposedVertices(self):
		exposed = []

		for v in range(self.graph.count()):
			if len(self.matching.adjacents(v)) == 0:
				exposed.append(v)

		return exposed

	#Queue edges from v to be processed
	def queueEdges(self, v):
		for adj in self.graph.adjacents(v):
			self.edgeQueue.append(Edge(v, adj))

	#Add the vertice 'v' to the 'forest', under the tree of vertice 'parent'
	#and its matched vertice
	def addMatchedVert(self, v, parent, forest):
		forest.putVert(v, parent)
		matched = self.getMatched(v);
		forest.putVert(matched, v)

		#Queue edges from matched vertices to be processed (he is an outer vertice)
		self.queueEdges(matched)

	# Build an algumenting path from the root of 'src' on the 'forest' to the
	# root of 'dst'.
	def makeAugmentPath(self, forest, src, dst):
		path = forest.makePathTo(src)
		path.extend(forest.makeReversePathTo(dst))
		return path

	def getMatched(self, v):
		return next(iter(self.matching.adjacents(v)))

class ContractedAugmentPathFinder(object):
	def __init__(self, graph, matching, blossom):
		self.graph = graph
		self.matching = matching

		# Contract graph and matching
		self.cGraph = self.contract(graph, blossom)
		self.cMatching = self.contract(matching, blossom)
		self.blossom = blossom

		print "Found blossom: ", blossom.path
		print "Contracted graph: \n", self.cGraph, "\n and contracted matching: \n", self.cMatching


	def findPath(self):
		p = AugmentPathFinder(self.cGraph, self.cMatching).findPath()

		if(not p):
			return p

		return self.expandPath(p, self.blossom, self.cGraph.count() - 1)

	def contract(self, graph, blossom):
		contracted = Graph(graph.count())
		# Add blossom vertice
		blossomV = contracted.addVertice()

		for v in range(graph.count()):
			if(blossom.hasVertice(v)):
				continue
			for adj in graph.adjacents(v):
				if(not blossom.hasVertice(adj)):
					contracted.addEdge(v, adj)
				else:
					contracted.addEdge(v, blossomV)

		return contracted

	'''Expand the 'path' using the vertice 'blossomV' from the given 'blossom' '''
	def expandPath(self, path, blossom, blossomV):
		blossomIdx = path.index(blossomV)

		#Gets the vertice that connects to the blossom
		outBlossomIdx = blossomIdx - 1 if blossomIdx > 0 else blossomIdx + 1
		outBlossomV = path[outBlossomIdx]

		#Search the vertex on blossom that connects with vertex outside of blossom
		blossomConn = self.searchBlossomConnection(blossom, outBlossomV);

		#Select the path on blossom that forms a alternating path with the vertex out of the blossom
		blossomAltPath = self.buildAlternatingPath(blossomConn, outBlossomV, blossom)

		#Replaces the blossom on the path
		path = path[:blossomIdx] + blossomAltPath + path[blossomIdx + 1 :]

		return path

	#Gets the vertice on blossom that connects with vertice 'connectionV'
	def searchBlossomConnection(self, blossom, connectionV):
		for v in self.graph.adjacents(connectionV):
			if blossom.hasVertice(v):
				return v
		return None

	def buildAlternatingPath(self, vInBlossom, outV, blossom):
		altPath = []
		pathLen = len(blossom.path)
		startIdx = blossom.path.index(vInBlossom)
		for i in range(pathLen):
			idx = (i + startIdx) % pathLen
			altPath.append(blossom.path[idx])


		revert = (self.matching.hasEdge(vInBlossom, outV) == self.matching.hasEdge(vInBlossom, altPath[1]))
		if revert:
			first = altPath.pop(0)
			altPath.reverse()
			altPath.insert(0, first)

		return altPath

	def _matchingPathToStr(self, path):
		out = str(path[0])
		for i in range(len(path) - 1):
			v1 = path[i]
			v2 = path[i + 1]
			edgeSymbol = " ======= " if self.matching.hasEdge(v1, v2) else " = = = = = "
			out += edgeSymbol + str(v2)

		return out

class Blossom(object):
	def __init__(self, root, path):
		self.root = root
		self.path = path
		self.verts = set()
		for v in path:
			self.verts.add(v)

	def __len__(self):
		return len(self.path)

	def hasVertice(self, v):
		return v in self.verts


	@staticmethod
	def makeBlossom(forest, v1, v2):
		path1 = forest.makePathTo(v1)
		path2 = forest.makePathTo(v2)

		blossomRoot = Blossom.findCommonAncestor(path1, path2)

		blossomPath = Blossom.makeBlossomPath(blossomRoot, path1, path2)

		return Blossom(blossomRoot, blossomPath)

	@staticmethod
	def findCommonAncestor(path1, path2):
		ancestorIdx = 0
		for i in range(min(len(path1), len(path2))):
			if(path1[i] != path2[i]):
				break
			ancestorIdx = i

		return path1[ancestorIdx]

	@staticmethod
	def makeBlossomPath(blossomRoot, path1, path2):
		startPath = path1[path1.index(blossomRoot) : ]
		finishPath = path2[path2.index(blossomRoot) : ]
		finishPath.reverse()

		blossomPath = startPath
		blossomPath.extend(finishPath)
		blossomPath.pop() #Removes last vertice (repeated)

		return blossomPath


class ForestNode(object):
	def __init__(self, vert, parent, root, outerNode):
		self.vert = vert
		self.parent = parent
		self.root = root
		self.isOuterNode = outerNode

class Forest(object):
	def __init__(self):
		self.nodes = dict()

	def addTree(self, vert):
		self.nodes[vert] = ForestNode(vert, None, vert, True)

	def putVert(self, vert, parent):
		parentNode = self.getNode(parent)
		self.nodes[vert] = ForestNode(vert, parent, parentNode.root, not parentNode.isOuterNode)

	def hasVert(self, vert):
		return self.nodes.has_key(vert)

	def getNode(self, vert):
		return self.nodes.get(vert)

	def isOuterNode(self, vert):
		return self.getNode(vert).isOuterNode

	def verticesAreOnSameTree(self, v1, v2):
		return self.getNode(v1).root == self.getNode(v2).root

	def makePathTo(self, vert):
		path = []
		node = self.nodes[vert]
		if node is not None :
			while(node.parent is not None):
				path.insert(0, node.vert)
				node = self.nodes[node.parent]
			path.insert(0, node.vert)

		return path

	def makeReversePathTo(self, vert):
		path = self.makePathTo(vert)
		path.reverse()
		return path

def main():
	if len(sys.argv) <= 1:
		print "Usage " + sys.argv[0] + " <graph file>"
		return

	g = graphs.GraphReader().readGraph(sys.argv[1])

	print "graph:\n ", g
	
	maximumMatching = BlossomMatching(g).findMaximumMatching()

	print
	print "Maximum Matching: \n", maximumMatching

if __name__=="__main__":
	main()
