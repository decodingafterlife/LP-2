class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, vertex_1, vertex_2):
        self.add_vertex(vertex_1)
        self.add_vertex(vertex_2)

        if vertex_2 not in self.adj_list[vertex_1]:
            self.adj_list[vertex_1].append(vertex_2)

        if vertex_1 not in self.adj_list[vertex_2]:
            self.adj_list[vertex_2].append(vertex_1)

    def dfs(self, start_vertex):
        visited = set()
        result = []
        stack = [start_vertex]

        while stack:
            vertex = stack.pop()

            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

            for neighbour in self.adj_list[vertex]:
                if neighbour not in visited:
                    stack.append(neighbour)

        return result

    def bfs(self, start_vertex):
        visited = set()
        queue = [start_vertex]
        result = []
        visited.add(start_vertex)

        while queue:
            vertex = queue.pop(0)
            result.append(vertex)
            for neighbour in self.adj_list[vertex]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return result
        
        
        

g = Graph()
    
    # Create vertices
vertices = ["A", "B", "C", "D", "E", "F", "G"]
for vertex in vertices:
    g.add_vertex(vertex)
    
    # Add edges to create an undirected graph
    # A -- B -- C
    # |    |    |
    # D -- E -- F
    # |
    # G
edges = [("A", "B"), ("A", "D"), ("B", "C"), ("B", "E"), 
             ("C", "F"), ("D", "E"), ("D", "G"), ("E", "F")]
    
for edge in edges:
    g.add_edge(edge[0], edge[1])
    

    

    
    # Perform DFS traversal (iterative)
print("\nDFS Traversal (Iterative) starting from 'A':")
print(g.dfs("A"))
    
    # Perform BFS traversal
print("\nBFS Traversal starting from 'A':")
print(g.bfs("A"))