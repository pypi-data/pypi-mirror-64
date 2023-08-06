class DirectedGraph:

	def __init__(self):
		'''Create an empty directed graph'''
		self.vertices = set()
		self.in_edges = dict()
		self.out_edges = dict()
	
	def add_vertex(self, vertex):
		'''Add vertex to graph
		
		Arguments:
			vertex: vertex to be added
		'''
		self.__validate_vertices(vertex, expected=False)
		self.vertices.add(vertex)
		self.in_edges[vertex] = dict()
		self.out_edges[vertex] = dict()
	
	def remove_vertex(self, vertex):
		'''Remove vertex from graph
		
		Arguments:
			vertex: vertex to be removed
		'''
		self.__validate_vertices(vertex)
		self.vertices.remove(vertex)
		for destination, edge in self.out_edges[vertex].items():
			del self.in_edges[destination][vertex]
		for source, edge in self.in_edges[vertex].items():
			del self.out_edges[source][vertex]
		del self.in_edges[vertex]
		del self.out_edges[vertex]
	
	def has_vertex(self, vertex):
		'''Check if graph has vertex
		
		Arguments:
			vertex: vertex to be checked
			
		Returns:
			bool: whether vertex is in graph or not
		'''
		return vertex in self.vertices
	
	def __len__(self):
		'''Get number of vertices'''
		return len(self.vertices)
	
	def iter_vertices(self):
		'''Iterate through vertices
		
		Yields:
			vertex in graph
		'''
		for vertex in self.vertices:
			yield vertex
	
	def add_edge(self, source, destination, edge):
		'''Add edge to graph
		
		Arguments:
			source: vertex from which the edge comes from
			destination: vertex to which the edge goes to
			edge: the edge itself
		'''
		self.__validate_vertices(source, destination)
		self.__validate_edges(source, destination, edge, expected=False)
		self.out_edges[source][destination] = edge
		self.in_edges[destination][source] = edge
	
	def remove_edge(self, source, destination):
		'''Remove edge from graph
		
		Arguments:
			source: vertex from which the edge comes from
			destination: vertex to which the edge goes to
		'''
		self.__validate_vertices(source, destination)
		self.__validate_edges(source, destination)
		del self.in_edges[destination][source]
		return self.out_edges[source].pop(destination)
	
	def has_edge(self, source, destination):
		'''Check if graph has edge
		
		Arguments:
			source: vertex from which the edge comes from
			destination: vertex to which the edge goes to
		'''
		return destination in self.out_edges[source]
	
	def get_edge(self, source, destination):
		'''Get edge between two vertices
		
		Arguments:
			source: vertex from which the edge comes from
			destination: vertex to which the edge goes to
			
		Returns:
			the edge from source to destination
		'''
		self.__validate_edges(source, destination)
		return self.out_edges[source][destination]
	
	def get_degree(self, source, i=False, o=True):
		'''Get number of neighbours
		
		Arguments:
			source: vertex
			
		Keyword arguments:
			i: count indegree
			o: count outdegree
			
		Returns:
			int: degree
		'''
		self.__validate_vertices(source)
		return ((len(self.in_edges[source])  if i else 0) +
				(len(self.out_edges[source]) if o else 0))
	
	def iter_neighbours(self, vertex, i=False, o=True):
		'''Iterate through neighbours
		
		Arguments:
			vertex: vertex whose neighbourhood will be iterated
		
		Keyword arguments:
			i: count outedges
			o: count inedges
			
		Yields:
			neighbour
			edge
			int: -1 if inedge, 1 if outedge
		'''
		self.__validate_vertices(vertex)
		if i: # edges going to 'vertex'
			for source, edge in self.in_edges[vertex].items():
				yield source, edge, -1
		if o: # edges coming from 'vertex'
			for destination, edge in self.out_edges[vertex].items():
				yield destination, edge, 1
	
	def dfs(self, vertex, visited=None, i=False, o=True):
		'''Perform a depth-first search
		
		Arguments:
			vertex: vertex from which the search begins
			visited: visited set or None if empty
			i: walk through inedges
			o: walk through inedges
		
		Yields:
			vertices in order of visit
		'''
		self.__validate_vertices(vertex)
		return self.__dfs(vertex, visited or set(), i, o)
	
	def __dfs(self, vertex, visited, i, o):
		if vertex not in visited:
			yield vertex
			visited.add(vertex)
			for neighbour, *_ in self.iter_neighbours(vertex, i, o):
				for neighbour2 in self.__dfs(neighbour, visited, i, o):
					yield neighbour2
	
	def bfs(self, vertex, visited=None, i=False, o=True):
		'''Perform a breadth-first search
		
		Arguments:
			vertex: vertex from which the search begins
			visited: visited set or None if empty
			i: walk through inedges
			o: walk through inedges
			
		Yields:
			vertices in order of visit
		'''
		self.__validate_vertices(vertex)
		from collections import deque
		bfs_deque = deque()
		visited = visited or set()
		if vertex not in visited:
			bfs_deque.append(vertex)
			visited.add(vertex)
			while len(bfs_deque) > 0:
				vertex = bfs_deque.popleft()
				yield vertex
				for neighbour, *_ in self.iter_neighbours(vertex, i, o):
					if neighbour not in visited:
						bfs_deque.append(neighbour)
						visited.add(neighbour)
	
	def __validate_vertices(self, *vertices, expected=True):
		for vertex in vertices:
			if self.has_vertex(vertex) != expected:
				raise Exception("Vertex '{}' is {} in graph".format(
								vertex, "not" if expected else "already"))
	
	def __validate_edges(self, source, destination, *edges, expected=True):
		if self.has_edge(source, destination) != expected:
			raise Exception("Edge between {} and {} is {} in graph".format(
							source, destination, "not" if expected else "already"))
		for edge in edges:
			if expected and (self.get_edge(source, destination) == edge) != expected:
				raise Exception("Edge '{}' between {} and {} is {} in graph".format(
								source, destination, edge, "not" if expected else "already"))

class UndirectedGraph(DirectedGraph):

	def add_edge(self, source, destination, edge):
		super().add_edge(source, destination, edge)
		super().add_edge(destination, source, edge)

	def remove_edge(self, source, destination):
		e1 = super().remove_edge(destination, source)
		e2 = super().remove_edge(source, destination)
		assert e1 == e2, "Inconsistency of edge representation"
		return e1

class GraphFactory:
	
	@staticmethod
	def get_empty_graph(size=10, directed=True):
		g = DirectedGraph() if directed else UndirectedGraph()
		for v in range(size):
			g.add_vertex(v)
		return g
	
	@staticmethod
	def get_full_graph(size=10, directed=True):
		g = GraphFactory.get_empty_graph(size, directed)
		for v in range(size):
			for w in range(size):
				g.add_edge(v, w, v*w)
		return g