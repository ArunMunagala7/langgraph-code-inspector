# Test Case: Binary Search Tree Operations
# Expected Quality: A-
# Expected Bugs: 0


from typing import Optional

class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BST:
    def __init__(self):
        self.root: Optional[TreeNode] = None
    
    def insert(self, val: int) -> None:
        """Insert value into BST."""
        if self.root is None:
            self.root = TreeNode(val)
        else:
            self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node: TreeNode, val: int) -> TreeNode:
        """Helper for recursive insertion."""
        if node is None:
            return TreeNode(val)
        
        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        elif val > node.val:
            node.right = self._insert_recursive(node.right, val)
        
        return node
    
    def search(self, val: int) -> bool:
        """Search for value in BST."""
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node: Optional[TreeNode], val: int) -> bool:
        """Helper for recursive search."""
        if node is None:
            return False
        
        if val == node.val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
    
    def delete(self, val: int) -> None:
        """Delete value from BST."""
        self.root = self._delete_recursive(self.root, val)
    
    def _delete_recursive(self, node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """Helper for recursive deletion."""
        if node is None:
            return None
        
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children
            min_node = self._find_min(node.right)
            node.val = min_node.val
            node.right = self._delete_recursive(node.right, min_node.val)
        
        return node
    
    def _find_min(self, node: TreeNode) -> TreeNode:
        """Find minimum value node in subtree."""
        current = node
        while current.left is not None:
            current = current.left
        return current
