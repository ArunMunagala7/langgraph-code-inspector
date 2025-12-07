# Test Case: Recursive Tree Traversal
# Expected Quality: A-
# Expected Bugs: 0


from typing import Optional, List

class TreeNode:
    def __init__(self, val: int, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Perform inorder traversal (left -> root -> right).
    
    Time: O(n), Space: O(h) where h is height
    """
    if root is None:
        return []
    
    result = []
    result.extend(inorder_traversal(root.left))
    result.append(root.val)
    result.extend(inorder_traversal(root.right))
    
    return result

def find_path(root: Optional[TreeNode], target: int) -> Optional[List[int]]:
    """Find path from root to target value."""
    if root is None:
        return None
    
    if root.val == target:
        return [root.val]
    
    # Search in left subtree
    left_path = find_path(root.left, target)
    if left_path is not None:
        return [root.val] + left_path
    
    # Search in right subtree
    right_path = find_path(root.right, target)
    if right_path is not None:
        return [root.val] + right_path
    
    return None
