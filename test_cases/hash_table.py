# Test Case: Hash Table with Chaining
# Expected Quality: B+
# Expected Bugs: 0


from typing import List, Optional, Tuple

class HashTable:
    def __init__(self, size: int = 10):
        """
        Initialize hash table with separate chaining.
        
        Time Complexity: O(1) average for insert/search/delete
        Space Complexity: O(n)
        """
        self.size = size
        self.table: List[List[Tuple[str, any]]] = [[] for _ in range(size)]
        self.count = 0
    
    def _hash(self, key: str) -> int:
        """Hash function using built-in hash."""
        return hash(key) % self.size
    
    def insert(self, key: str, value: any) -> None:
        """Insert key-value pair."""
        index = self._hash(key)
        
        # Update if key exists
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        
        # Insert new key-value pair
        self.table[index].append((key, value))
        self.count += 1
        
        # Rehash if load factor > 0.7
        if self.count / self.size > 0.7:
            self._rehash()
    
    def get(self, key: str) -> Optional[any]:
        """Get value for key."""
        index = self._hash(key)
        
        for k, v in self.table[index]:
            if k == key:
                return v
        
        return None
    
    def delete(self, key: str) -> bool:
        """Delete key-value pair."""
        index = self._hash(key)
        
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.count -= 1
                return True
        
        return False
    
    def _rehash(self) -> None:
        """Resize and rehash all entries."""
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)
