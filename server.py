"""
I dont know if any of the stuff below was supposed to go in main,
but feel free to move it.

I tested the cost function with a small test file, and it seems to be working.
"""
# Import class file
import digraph

# Create a set of edges from text file
print("Constructing Graph")
edges = digraph.edges_from_text("edmonton-roads-digraph.txt")
graph = digraph.Digraph(edges)
print("Done")

# Find the cost distance using vertices from edge
def cost_distance(e):
    """
    >>> E = digraph.edges_from_text("test.txt")
    >>> G = digraph.Digraph(edges)
    >>> C = cost_distance( (276281417,276281415) )
    >>> C
    0.0008483923856308028
       
    """
    for (start, stop, cost) in edges:
        if start == e[0] and stop == e[1]:
            return cost

if __name__ == "__main__":
    import doctest
    doctest.testmod()
