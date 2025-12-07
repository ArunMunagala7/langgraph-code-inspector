# Test Case: Potential Memory Issues
# Expected Quality: D+
# Expected Bugs: 3


class Cache:
    def __init__(self):
        # Bug 1: Unbounded cache growth - memory leak
        self.data = {}
    
    def set(self, key, value):
        self.data[key] = value
    
    def get(self, key):
        return self.data.get(key)

# Bug 2: Circular reference
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []
    
    def add_child(self, child):
        child.parent = self  # Circular reference
        self.children.append(child)

# Bug 3: Not closing file handles
def read_files(filenames):
    contents = []
    for fname in filenames:
        f = open(fname, 'r')  # Not closed!
        contents.append(f.read())
    return contents
