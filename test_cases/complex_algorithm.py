# Test Case: Complex Algorithm - Dijkstra's Shortest Path
# Expected Quality: B+
# Expected Bugs: 0


import heapq
from typing import Dict, List, Tuple

def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> Dict[int, int]:
    """
    Find shortest paths from start node to all other nodes.
    
    Args:
        graph: Adjacency list {node: [(neighbor, weight), ...]}
        start: Starting node
        
    Returns:
        Dictionary of shortest distances {node: distance}
    """
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        if current_dist > distances[current_node]:
            continue
        
        for neighbor, weight in graph.get(current_node, []):
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances
