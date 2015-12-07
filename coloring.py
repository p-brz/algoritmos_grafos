#! /usr/bin/env python

import graphs
from graphs import *
import sys

MAX_COLORS = 10

class GraphColoring(object):
	def __init__(self, graph):
		self.graph = graph
		self.coloring = Coloring(graph.count())

	def findColoring(self):
		if(self.graph.count() == 0):
			return 0;

		colorCount = 2
		while not self.tryColoring(colorCount, 0, 0) and colorCount < MAX_COLORS:
			colorCount += 1
			self.coloring.clear()

		return colorCount

	def tryColoring(self, colorCount, vertice, color):
		self.coloring.putColor(vertice, color)

		for adj in self.graph.adjacents(vertice):
			if(self.coloring.hasColor(adj)):
				if self.coloring.getColor(adj) != color:
					#Vertice ja tem cor, mas eh diferente desta, entao passa para o proximo
					continue

				#nao tem como pintar este vertice com esta cor
				self.coloring.removeColor(vertice)
				return False

			colored = self.tryColorWithOtherColors(adj, colorCount, color)
			if not colored:
				self.coloring.removeColor(vertice)
				return False;

		#conseguiu pintar todos os vertices
		return True

	def tryColorWithOtherColors(self, v, colorCount, color):
		for otherColor in range(colorCount):
			if(otherColor == color):
				continue
			if(self.tryColoring(colorCount, v, otherColor)):
				return True

		return False

class Coloring(object):
	COLORS_MAPPING = ['RED', 'GREEN', 'BLUE', 'YELLOW', 'BLACK', 'WHITE']

	def __init__(self, count):
		self.count  = count
		self.clear()

	def clear(self):
		self.coloring = []
		for i in range(self.count):
			self.coloring.append(None)

	def hasColor(self, vertice):
		return self.coloring[vertice] is not None

	def getColor(self, vertice):
		return self.coloring[vertice]

	def putColor(self, vertice, color):
		self.coloring[vertice] = color

	def removeColor(self, vertice):
		self.coloring[vertice] = None

	def __str__(self):
		out = ""
		idx = 0
		for c in self.coloring:
			out += str(idx) + ": "
			if c is None :
				out += str(c)
			elif c < len(Coloring.COLORS_MAPPING):
				out += Coloring.COLORS_MAPPING[c]
			else:
				out += "COLOR(" + str(c) + ")"
			out +="\n"

			idx+=1

		return out

def main():
	if len(sys.argv) <= 1:
		print "Usage " + sys.argv[0] + " <graph file>"
		return

	g = graphs.GraphReader().readGraph(sys.argv[1])

	print "graph:\n",g

	graphColoring = GraphColoring(g)
	colorCount = graphColoring.findColoring()

	print
	print "found with ", colorCount, " colors"
	print "Coloring: \n", graphColoring.coloring

if __name__=="__main__":
	main()
