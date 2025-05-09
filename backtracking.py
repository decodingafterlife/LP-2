class GraphColoringCSP:
    def __init__(self, graph, m):
        self.graph = graph  # Adjacency list
        self.V = len(graph)
        self.m = m  # Number of colors
        self.colors = [0] * self.V
        self.solutions = []

    def is_safe(self, v, c):
        for neighbor in self.graph[v]:
            if self.colors[neighbor] == c:
                return False
        return True

    def backtrack(self, v=0):
        # If all vertices are assigned a color
        if v == self.V:
            self.solutions.append(self.colors[:])
            return True  # You can return False here to find all solutions

        for c in range(1, self.m + 1):
            if self.is_safe(v, c):
                self.colors[v] = c
                if self.backtrack(v + 1):
                    return True  # Comment this if you want to find all solutions
                self.colors[v] = 0  # Backtrack

        return False

    def solve(self):
        if not self.backtrack():
            print("No solution exists")
        else:
            print("One possible solution:")
            print(self.colors)

# Example usage:
# Graph represented as an adjacency list (undirected)
graph = {
    0: [1, 2],
    1: [0, 2, 3],
    2: [0, 1],
    3: [1]
}

m = 3  # Number of colors
csp_solver = GraphColoringCSP(graph, m)
csp_solver.solve()
