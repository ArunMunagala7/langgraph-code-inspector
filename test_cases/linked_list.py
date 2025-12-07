# Test Case: Linked List Implementation
# Expected Quality: B+
# Expected Bugs: 0


from typing import Optional

class Node:
    def __init__(self, data):
        self.data = data
        self.next: Optional[Node] = None


class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self.size = 0
    
    def append(self, data) -> None:
        """Add element to end of list."""
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def prepend(self, data) -> None:
        """Add element to beginning of list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def delete(self, data) -> bool:
        """Delete first occurrence of data."""
        if self.head is None:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def reverse(self) -> None:
        """Reverse the linked list in-place."""
        prev = None
        current = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev
    
    def find_middle(self) -> Optional[Node]:
        """Find middle node using slow-fast pointer."""
        if self.head is None:
            return None
        
        slow = fast = self.head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        return slow
    
    def has_cycle(self) -> bool:
        """Detect cycle using Floyd's algorithm."""
        if self.head is None:
            return False
        
        slow = fast = self.head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                return True
        
        return False
