import heapq

from heuristics import euclidean


def search(finder, start_node, end_node, clearance, to_clear):
    def is_walkable(x, y):
        return finder.grid.is_walkable(x, y, finder.walkable, clearance)

    openlist = []

    def jump(node, parent):
        """
            Searches for a jump point (or a turning point) in a specific direction.
            This is a generic translation of the algorithm 2 in the paper:
              http://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf
            The current expanded node is a jump point if near a forced node
            In case diagonal moves are forbidden, when lateral nodes (perpendicular to
            the direction of moves are walkable, we force them to be turning points in other
            to perform a straight move.
        """
        if not node:
            return None

        x, y = node.x, node.y
        if not is_walkable(x, y):
            return None

        if node == end_node:
            return node

        dx, dy = x - parent.x, y - parent.y

        if dx != 0 and dy != 0:
            # Current node is a jump point if one of his leftside/rightside neighbours ahead is forced
            if (is_walkable(x-dx, y+dy) and not is_walkable(x-dx, y)) or \
               (is_walkable(x+dx, y-dy) and not is_walkable(x, y-dy)):
                return node

            if jump(finder.grid.get_node_at(x+dx, y), node):
                return node
            if jump(finder.grid.get_node_at(x, y+dy), node):
                return node

        elif dx != 0:
            # Search along X-axis case
            if finder.allow_diagonal:
                walkable_by_diagonal = (is_walkable(x + dx, y + 1) and not is_walkable(x, y + 1)) or \
                                       (is_walkable(x + dx, y - 1) and not is_walkable(x, y - 1))
                if walkable_by_diagonal:
                    return node
            else:
                walkable_by_horizontal_sides = is_walkable(x+1, y) or is_walkable(x-1, y)
                if walkable_by_horizontal_sides:
                    return node
        else:
            # Search along Y-axis case
            if finder.allow_diagonal:
                walkable_by_diagonal = (is_walkable(x + 1, y + dy) and not is_walkable(x+1, y)) or \
                                       (is_walkable(x - 1, y + dy) and not is_walkable(x-1, y))
                if walkable_by_diagonal:
                    return node
            else:
                walkable_by_vertical_sides = is_walkable(x, y + 1) or is_walkable(x, y - 1)
                if walkable_by_vertical_sides:
                    return node

        if finder.allow_diagonal:
            if is_walkable(x+dx, y) or is_walkable(x, y+dy):
                return jump(finder.grid.get_node_at(x+dx, y+dy), node)


    def identify_successors(node):
        """
        Searches for successors of a given node in the direction of each of its neighbours.
        This is a generic translation of the algorithm 1 in the paper:
          http://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf
        Also, we notice that processing neighbours in a reverse order producing a natural
        looking path, as the pathfinder tends to keep heading in the same direction.
        In case a jump point was found, and this node happened to be diagonal to the
        node currently expanded in a straight mode search, we skip this jump point.
        """
        neighbours = find_neighbours(finder, node, clearance)
        neighbours.reverse()
        for neighbour in neighbours:
            skip = False
            jump_node = jump(neighbour, node)

            if jump_node and not finder.allow_diagonal:
                if jump_node.x != node.x and jump_node.y != node.y:
                    skip = True

            # Perform regular A* on a set of jump points
            if jump_node and not skip and not jump_node.closed:
                # Update the jump node and move it in the closed list if it wasn't there
                extraG = euclidean(jump_node, node)
                new_g = node.g + extraG
                if not jump_node.opened or new_g < jump_node.g:
                    to_clear[jump_node] = True
                    jump_node.g = new_g
                    jump_node.h = jump_node.h or finder.heuristic(jump_node, end_node)
                    jump_node.parent = node
                    if not jump_node.opened:
                        heapq.heappush(openlist, jump_node)
                        jump_node.open()
                    else:
                        heapq.heapify(openlist)

    start_node.g = start_node.h = 0
    heapq.heappush(openlist, start_node)
    start_node.open()
    to_clear[start_node] = True

    while openlist:
        node = heapq.heappop(openlist)
        node.close()
        if node == end_node:
            return node
        identify_successors(node)

    return None

def find_neighbours(finder, node, clearance):
    """
    Looks for the neighbours of a given node.
    Returns its natural neighbours plus forced neighbours when the given
    node has no parent (generally occurs with the starting node).
    Otherwise, based on the direction of move from the parent, returns
    neighbours while pruning directions which will lead to symmetric paths.
    In case diagonal moves are forbidden, when the given node has no
    parent, we return straight neighbours (up, down, left and right).
    Otherwise, we add left and right node (perpendicular to the direction
    of move) in the neighbours list.
    """
    def is_walkable(x, y):
        return finder.grid.is_walkable(x, y, finder.walkable, clearance)

    if node.parent:
        # Node has a parent, we will prune some neighbours
        # Gets the direction of move
        neighbours = []
        x, y = node.x, node.y
        dx = (x - node.parent.x) // max(abs(x - node.parent.x), 1)
        dy = (y - node.parent.y) // max(abs(y - node.parent.y), 1)

        # Diagonal move case
        if dx != 0 and dy != 0:
            walkX = walkY = False
            if is_walkable(x, y + dy):
                neighbours.append(finder.grid.get_node_at(x, y + dy))
                walkY = True
            if is_walkable(x + dx, y):
                neighbours.append(finder.grid.get_node_at(x + dx, y))
                walkX = True

            if walkX or walkY:
                neighbours.append(finder.grid.get_node_at(x + dx, y + dy))

            if not is_walkable(x - dx, y) and walkY:
                neighbours.append(finder.grid.get_node_at(x - dx, y + dy))

            if not is_walkable(x, y - dy) and walkX:
                neighbours.append(finder.grid.get_node_at(x + dx, y - dy))

        # Move along Y-axis case
        elif dx == 0:
            if is_walkable(x, y + dy):
                neighbours.append(finder.grid.get_node_at(x, y + dy))

                if not is_walkable(x + 1, y):
                    neighbours.append(finder.grid.get_node_at(x + 1, y + dy))
                if not is_walkable(x - 1, y):
                    neighbours.append(finder.grid.get_node_at(x - 1, y + dy))

            # In case diagonal moves are forbidden, it needs to be optimized
            if not finder.allow_diagonal:
                if is_walkable(x + 1, y):
                    neighbours.append(finder.get_node_at(x + 1, y))
                if is_walkable(x - 1, y):
                    neighbours.append(finder.grid.get_node_at(x - 1, y))

        else:
            # Move along the X-axis case
            if is_walkable(x+dx, y):
                neighbours.append(finder.grid.get_node_at(x + dx, y))

                if not is_walkable(x, y + 1):
                    neighbours.append(finder.grid.get_node_at(x + dx, y + 1))
                if not is_walkable(x, y - 1):
                    neighbours.append(finder.grid.get_node_at(x + dx, y - 1))

            # In case diagonal moves are forbidden, it needs to be optimized
            if not finder.allow_diagonal:
                if is_walkable(x, y + 1):
                    neighbours.append(finder.get_node_at(x, y + 1))
                if is_walkable(x, y - 1):
                    neighbours.append(finder.grid.get_node_at(x, y - 1))

        return [n for n in neighbours if n]

    return finder.grid.get_neighbours(node, finder.walkable, finder.allow_diagonal, finder.tunneling, clearance)
