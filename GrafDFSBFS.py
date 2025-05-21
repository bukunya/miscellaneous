def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(f"Visited: {start}")
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

def bfs(graph, start):
    visited = set([start])
    queue = [start]
    while queue:
        vertex = queue.pop(0)
        print(f"Visited: {vertex}")
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

def print_graph(graph):
    print("Struktur Graf:")
    for vertex, neighbors in graph.items():
        print(f"{vertex}: {neighbors}")
    print()

if __name__ == "__main__":
    graf = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    print_graph(graf)
    print("Traversal DFS dimulai dari node 'A':")
    dfs(graf, 'A')
    print("\nTraversal BFS dimulai dari node 'A':")
    bfs(graf, 'A')
    graf2 = {
        '5': ['3', '7'],
        '3': ['2', '4'],
        '7': ['8'],
        '2': [],
        '4': ['8'],
        '8': []
    }
    print("\n\nContoh graf lain:")
    print_graph(graf2)
    print("Traversal DFS dimulai dari node '5':")
    dfs(graf2, '5')
    print("\nTraversal BFS dimulai dari node '5':")
    bfs(graf2, '5')
