# Test Case: Min Heap Implementation
# Expected Quality: A-
# Expected Bugs: 0


from typing import List

class MinHeap:
    def __init__(self):
        """
        Initialize min heap.
        
        Time Complexity: O(log n) for insert/extract_min
        Space Complexity: O(n)
        """
        self.heap: List[int] = []
    
    def parent(self, i: int) -> int:
        return (i - 1) // 2
    
    def left_child(self, i: int) -> int:
        return 2 * i + 1
    
    def right_child(self, i: int) -> int:
        return 2 * i + 2
    
    def swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def insert(self, value: int) -> None:
        """Insert value into heap."""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
    
    def _heapify_up(self, i: int) -> None:
        """Restore heap property upward."""
        while i > 0 and self.heap[i] < self.heap[self.parent(i)]:
            self.swap(i, self.parent(i))
            i = self.parent(i)
    
    def extract_min(self) -> int:
        """Remove and return minimum element."""
        if not self.heap:
            raise IndexError("Heap is empty")
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        
        return min_val
    
    def _heapify_down(self, i: int) -> None:
        """Restore heap property downward."""
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        if left < len(self.heap) and self.heap[left] < self.heap[min_index]:
            min_index = left
        
        if right < len(self.heap) and self.heap[right] < self.heap[min_index]:
            min_index = right
        
        if min_index != i:
            self.swap(i, min_index)
            self._heapify_down(min_index)
    
    def peek(self) -> int:
        """Return minimum without removing."""
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]
    
    def size(self) -> int:
        return len(self.heap)
