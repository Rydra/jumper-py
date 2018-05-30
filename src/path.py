from heuristics import euclidean


class Path:
    def __init__(self):
        self.nodes = []
        self.grid = None

    def __iter__(self):
        for node in self.nodes:
            yield node

    @property
    def length(self):
        path_length = 0
        for i in range(1, len(self.nodes)):
            path_length += euclidean(self.nodes[i], self.nodes[i - 1])

        return path_length

    def fill(self, grid):
        """
        `Path` filling modifier. Interpolates between non contiguous nodes along a `path`
        to build a fully continuous `path`. This maybe useful when using search algorithms such as Jump Point Search.
        """
        i = 2
        n = len(self.nodes)
        while True:
            xi, yi = self.nodes[i].x, self.nodes[i].y
            previous_node = self.nodes[i-1]
            dx, dy = xi-previous_node.x, yi-previous_node.y
            if abs(dx) > 1 or abs(dy) > 1:
                incrX = dx / max(abs(dx), 1)
                incrY = dy / max(abs(dy), 1)
                self.nodes.insert(i, grid.get_node_at(previous_node.x + incrX, previous_node.y + incrY))
                n += 1
            else:
                i += 1
            if i > n:
                break

    def filter(self):
        """
        `Path` compression modifier. Given a `path`, eliminates useless nodes to return a lighter `path`
        consisting of straight moves. Does the opposite of @{Path:fill}
        """
        i = 2
        xi, yi = self.nodes[i].x, self.nodes[i].y
        dx, dy = xi - self.nodes[i-1].x, yi - self.nodes[i-1].y

        while True:
            old_dx, old_dy = dx, dy
            try:
                i += 1
                xi, yi = self.nodes[i].x, self.nodes[i].y
                dx, dy = xi - self.nodes[i - 1].x, yi - self.nodes[i - 1].y
                if old_dx == dx and old_dy == dy:
                    del self.nodes[i-1]
            except IndexError:
                break

    def add_node(self, node):
        self.nodes.append(node)

    def __add__(self, other):
        for node in other.nodes:
            self.add_node(node)

        return self

    def reverse(self):
        self.nodes = self.nodes.reverse()
