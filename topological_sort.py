import graphs
import directed_cycle

class TopologicalSort(directed_cycle.DirectedCycleDetector):
	def _super(self):
		return super(self.__class__, self)

	def __init__(self, graph, ignoreCycles=False):
		self._super().__init__(graph)
		self._resetOrder()
		self.ignoreCycles = ignoreCycles

	def _resetOrder(self):
		self.order = []

	def sort(self):
		self._resetOrder()
		# Percorre grafo enquanto checa por ciclos
		self.checkCycle()
		if(self.hasCycle()): #invalida ordem, caso ciclo seja encontrado
			self.order = None

		return self.order

	def onVisit(self, vertice):
		if not self.ignoreCycles:
			self._super().onVisit(vertice)

	def onFinishVisit(self, vertice):
		if not self.ignoreCycles:
			self._super().onFinishVisit(vertice)
		self.order.insert(0, vertice)

import sys

def main():
	if len(sys.argv) <= 1:
		return

	g = graphs.DirectedGraphReader().readGraph(sys.argv[1])
	topolSort = TopologicalSort(g)
	topolOrder = topolSort.sort()

	if(topolOrder):
		print "Topological order:\n %s" % topolOrder
	else:
		print "Graph is not acyclic, and cannot be ordered"
		print "cycle found: %s" % topolSort.getCycle()

	print g

if __name__=="__main__":
	main()
