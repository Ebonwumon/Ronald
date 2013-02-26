"""
Graph module for undirected graphs.
"""

import random

try:
    import display
except:
    print("Warning: failed to load display module.  Graph drawing will not work.")
    
class Digraph:
    """
    Directed graph.  The vertices must be immutable.

    To create an empty graph:
    >>> G = Digraph()
    >>> (G.num_vertices(), G.num_edges())
    (0, 0)

    To create a circular graph with 3 vertices:
    >>> G = Digraph([(1, 2), (2, 3), (3, 1)])
    >>> (G.num_vertices(), G.num_edges())
    (3, 3)
    """

    def __init__(self, edges = None):
        self._tosets = {}
        self._fromsets = {}

        if edges:
            for e in edges: self.add_edge(e)

    def __repr__(self):
        return "Digraph({}, {})".format(self.vertices(), self.edges())

    def add_vertex(self, v):
        """
        Adds a vertex to the graph.  It starts with no edges.
        
        >>> G = Digraph()
        >>> G.add_vertex(1)
        >>> G.vertices() == {1} 
        True
        """
        if v not in self._tosets:
            self._tosets[v] = set()
            self._fromsets[v] = set()

    def add_edge(self, e):
        """
        Adds an edge to graph.  If vertices in the edge do not exist, it adds them.
        
        >>> G = Digraph()
        >>> G.add_vertex(1)
        >>> G.add_vertex(2)
        >>> G.add_edge((1, 2))
        >>> G.add_edge((2, 1))
        >>> G.add_edge((3, 4))
        >>> G.add_edge((1, 2))
        >>> G.num_edges()
        3
        >>> G.num_vertices()
        4
        """
        # Adds the vertices (in case they don't already exist)
        for v in e:
            self.add_vertex(v)

        # Add the edge
        self._tosets[e[0]].add(e[1])
        self._fromsets[e[1]].add(e[0])

    def edges(self):
        """
        Returns the set of edges in the graph as ordered tuples.
        """
        return { (v, w) for v in self._tosets for w in self._tosets[v] }

    def vertices(self):
        """
        Returns the set of vertices in the graph.
        """
        return set(self._tosets.keys())

    def draw(self, filename, attr = {}):
        """
        Draws the graph into a dot file.
        """
        display.write_dot_desc((self.vertices(), self.eges()), filename, attr)

    def num_edges(self):
        m = 0
        for v in self._tosets:
            m += len(self._tosets[v])
        return m

    def num_vertices(self):
        """
        Returns the number of vertices in the graph.
        """
        return len(self._tosets)

    def adj_to(self, v):
        """
        Returns the set of vertices that contain an edge from v.

        >>> G = Digraph()
        >>> for v in [1, 2, 3]: G.add_vertex(v)
        >>> G.add_edge((1, 3))
        >>> G.add_edge((1, 2))
        >>> G.adj_to(3) == set() 
        True
        >>> G.adj_to(1) == { 2, 3 }
        True
        """
        return self._tosets[v]

    def adj_from(self, v):
        """
        Returns the set of vertices that contain an edge to v.

        >>> G = Digraph()
        >>> G.add_edge((1, 3))
        >>> G.add_edge((2, 3))
        >>> G.adj_from(1) == set() 
        True
        >>> G.adj_from(3) == { 1, 2 }
        True
        """
        return self._fromsets[v]

    def is_path(self, path):
        """
        Returns True if the list of vertices in the argument path are a
        valid path in the graph.  Returns False otherwise.

        >>> G = Digraph([(1, 2), (2, 3), (2, 4), (1, 5), (2, 5), (4, 5), (5, 2)])
        >>> G.is_path([1, 5, 2, 4, 5])
        True

        # Not a path
        >>> G.is_path([1, 5, 4, 2])
        False

        # Try giving one edge
        >>> G.is_path([2,3])
        True
        
        # Try giving an empty list
        >>> G.is_path([])
        The path is empty
        False

        # What if path is a circle?
        >>> G = Digraph([(1,2), (2,3), (3,1)])
        >>> G.is_path([1, 2, 3, 1, 2, 3])
        True

        
        """
        # Make sure path has items in it.
        # If it is empty, return False
        if len(path) == 0:
            print( "The path is empty" )
            return False
        
        # Create a list of edges based on path
        path_edges = []
        for i in range( len(path)-1 ):
            if (path[i], path[i+1]) not in path_edges:
                path_edges.append( (path[i], path[i+1]) )

        # Compare list of path to list edges of graph
        for pair in path_edges:
            # As soon as an edge does not match, not a path
            if pair not in self.edges():
                return False

        # If all edges are in list of graph edges, it is a path
        return True

def random_graph(n, m):
    """
    Make a random Digraph with n vertices and m edges.

    >>> G = random_graph(10, 5)
    >>> G.num_edges()
    5
    >>> G.num_vertices()
    10
    >>> G = random_graph(1, 1)
    Traceback (most recent call last):
    ...
    ValueError: For 1 vertices, you wanted 1 edges, but can only have a maximum of 0
    """
    G = Digraph()
    for v in range(n):
        G.add_vertex(v)

    max_num_edges = n * (n-1)
    if m > max_num_edges:
        raise ValueError("For {} vertices, you wanted {} edges, but can only have a maximum of {}".format(n, m, max_num_edges))

    while G.num_edges() < m:
        G.add_edge(random.sample(range(n), 2))

    return G

def spanning_tree(G, start):  
    """ 
    Runs depth-first-search on G from vertex start to create a spanning tree.
    """
    visited = set()
    todo = [ (start, None) ]

    T = Digraph()
    
    while todo:
        (cur, e) = todo.pop()

        if cur in visited: continue

        visited.add(cur)
        if e: T.add_edge(e)

        for n in G.adj_to(cur):
            if n not in visited:
                todo.append((n, (cur, n)))
                
    return T

def shortest_path(G, source, dest):
    """
    Returns the shortest path from vertex source to vertex dest.

    >>> G = Digraph([(1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (3, 6), (6, 7)])
    >>> path = shortest_path(G, 1, 7)
    >>> path
    [1, 6, 7]
    >>> G.is_path(path)
    True

    >>> G = Digraph([(1, 2), (1, 3), (2, 4), (3, 5), (5, 4)])
    >>> path = shortest_path(G, 1, 4)
    >>> path
    [1, 2, 4]
    >>> G.is_path(path)
    True

    # No path to Dest (not connected)
    >>> G = Digraph([(1, 2), (2, 3), (1, 3), (4,5)])
    >>> path = shortest_path(G, 1, 5)
    >>> path
    []
    >>> G.is_path(path)
    The path is empty
    False

    # Source is dest
    >>> G = Digraph([(1, 2), (1, 3), (2, 4)])
    >>> path = shortest_path(G, 1, 1)
    >>> path
    [1]
    >>> G.is_path(path)
    True

    # Try a graph with many loops
    >>> G = Digraph([(1,2), (2,1), (2,3), (3,2), (3,4)])
    >>> path = shortest_path(G, 1, 4)
    >>> path
    [1, 2, 3, 4]
    >>> G.is_path(path)
    True
    
    """
    # Create a list to hold queue and a visited set to
    # hold tuples (vertex, leading) where leading is the
    # vertex that brought us to the vertex
    queue = [source]
    visited = [source]
    shortest_path = []
    parent = {}

    # If source = dest, return source
    if source == dest:
        return queue

    while queue:
        # Grab oldest element of queue
        v = queue[0]

        # Find unvisited neigbours
        for x in G.adj_to(v):

            # First check if a neighbour is destination
            if x == dest:

                # Build the path we just found
                cur_path = [dest, v]
                cur = v
                while source not in cur_path:
                    cur_path.append(parent[cur])
                    cur = parent[cur]
                                
                # Path is backwards, flip order
                cur_path.reverse()

                # If this is first path found, it is shortest so far
                if len(shortest_path) == 0 or len(cur_path) < len(cur_path):
                    shortest_path = cur_path

            # If neighbour is not dest:
            elif x not in visited:
                visited.append(x)
                queue.append(x)
                parent[x] = v

        # Remove v from queue
        queue.remove(v)

    return shortest_path
        
    
def compress(walk):
    """
    Remove cycles from a walk to create a path.
    
    >>> compress([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> compress([1, 3, 0, 1, 6, 4, 8, 6, 2])
    [1, 6, 2]
    """
    
    lasttime = {}

    for (i,v) in enumerate(walk):
        lasttime[v] = i

    rv = []
    i = 0
    while (i < len(walk)):
        rv.append(walk[i])
        i = lasttime[walk[i]]+1

    return rv
    

def least_cost_path(G, start, dest, cost):
    """
    >>> G = Digraph( [(1,2), (2,3)] )
    >>> s = least_cost_path(G, 1, 3, (lambda x: 1) )
    >>> s == [1, 2, 3]
    True

    """
    todo = {start: 0}
    visited = set()
    parent = {}

    while todo and dest not in visited:
        # get smallest from todo
        (cur,c) = ( min(todo.items(), key = lambda i: i[1]) )
        todo.pop(cur)
        visited.add(cur)
        for x in G.adj_to(cur):
            if x in visited: continue
            
            elif (x not in todo) or (c+cost((cur,x))<todo[x]):
                todo[x] = (c + cost( (cur,x) ))
                parent[x] = cur
                
            else: pass
                
    #extract path to dest
    path = [dest]
    while start not in path:
        path.append(parent[cur])
        cur = parent[cur]

    path.reverse()

    return path

if __name__ == "__main__":
    import doctest
    doctest.testmod()
