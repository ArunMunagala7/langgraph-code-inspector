# Test Case: Trie (Prefix Tree)
# Expected Quality: A-
# Expected Bugs: 0


from typing import Dict, List

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False


class Trie:
    """
    Trie data structure for efficient string operations.
    
    Time Complexity: O(m) for insert/search/delete where m is word length
    Space Complexity: O(n * m) where n is number of words
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert word into trie."""
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """Search for exact word in trie."""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with prefix."""
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> TrieNode:
        """Find node corresponding to prefix."""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def find_words_with_prefix(self, prefix: str) -> List[str]:
        """Find all words starting with prefix."""
        node = self._find_node(prefix)
        
        if node is None:
            return []
        
        words = []
        self._collect_words(node, prefix, words)
        return words
    
    def _collect_words(self, node: TrieNode, current: str, words: List[str]) -> None:
        """Recursively collect all words from node."""
        if node.is_end_of_word:
            words.append(current)
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, current + char, words)
    
    def delete(self, word: str) -> bool:
        """Delete word from trie."""
        return self._delete_recursive(self.root, word, 0)
    
    def _delete_recursive(self, node: TrieNode, word: str, index: int) -> bool:
        """Helper for recursive deletion."""
        if index == len(word):
            if not node.is_end_of_word:
                return False
            
            node.is_end_of_word = False
            return len(node.children) == 0
        
        char = word[index]
        if char not in node.children:
            return False
        
        child_node = node.children[char]
        should_delete = self._delete_recursive(child_node, word, index + 1)
        
        if should_delete:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end_of_word
        
        return False
