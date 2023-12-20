class Stack():
    def __init__(self):
        self._stack = []
        
    def push(self, item):
        self._stack.append(item)
        
    def isEmpty(self):
        return not self._stack

    def pop(self):
        if(self.isEmpty()):
            return None
        return self._stack.pop()

    def top(self):
        if(self.isEmpty()):
            return None
        return self._stack[-1]

    def size(self):
        return len(self._stack)

    def to_string(self):
        toString = ""
        for element in self._stack:
            toString += f"{element} "
        return toString