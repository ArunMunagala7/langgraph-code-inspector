# Test Case: Graph BFS and DFS
# Expected Quality: A
# Expected Bugs: 0


from typing import Dict, List, Set
from collections import deque

class Graph:
    def __init__(self):
        """Initialize graph as adjacency list."""
        self.graph: Dict[int, List[int]] = {}
    
    def add_edge(self, u: int, v: int) -> None:
        """Add edge from u to v."""
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        
        self.graph[u].append(v)
    
    def bfs(self, start: int) -> List[int]:
        """
        Breadth-first search traversal.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        if start not in self.graph:
            return []
        
        visited: Set[int] = set()
        queue = deque([start])
        result = []
        
        visited.add(start)
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start: int) -> List[int]:
        """
        Depth-first search traversal (iterative).
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        if start not in self.graph:
            return []
        
        visited: Set[int] = set()
        stack = [start]
        result = []
        
        while stack:
            node = stack.pop()
            
            if node not in visited:
                visited.add(node)
                result.append(node)
                
                # Add neighbors in reverse order for correct traversal
                for neighbor in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    def dfs_recursive(self, start: int, visited: Set[int] = None) -> List[int]:
        """Depth-first search (recursive)."""
        if visited is None:
            visited = set()
        
        if start not in self.graph or start in visited:
            return []
        
        visited.add(start)
        result = [start]
        
        for neighbor in self.graph[start]:
            result.extend(self.dfs_recursive(neighbor, visited))
        
        return result
    
    def has_path(self, start: int, end: int) -> bool:
        """Check if path exists between two nodes."""
        if start not in self.graph:
            return False
        
        visited: Set[int] = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            node = queue.popleft()
            
            if node == end:
                return True
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False
