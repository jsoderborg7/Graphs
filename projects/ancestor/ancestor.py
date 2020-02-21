from util import Queue

def earliest_ancestor(ancestors, starting_node):

    earliest_ancestor = -1
    current_length = 0

    # Adjacency list for all nodes/edges in ancestors
    ancestor_dictionary = {}

    # Add all nodes and edges to adjacency list
    for a in ancestors:
        if a[0] in ancestor_dictionary:
            ancestor_dictionary[a[0]].add(a[1])
        else:
            ancestor_dictionary[a[0]] = set()
            ancestor_dictionary[a[0]].add(a[1])
    
    # Begin BFS
    queue = Queue()
    visited = set()
    queue.enqueue([starting_node])
    while queue.size() > 0:
        current_path = queue.dequeue()
        current_node = current_path[-1]
        if current_node != starting_node:
            if len(current_path) > current_length:
                earliest_ancestor = current_node
                current_length = len(current_path)
            elif len(current_path) == current_length and earliest_ancestor > current_node:
                earliest_ancestor = current_node
        if current_node not in visited:
            visited.add(current_node)
            edges = []
            for x in ancestor_dictionary:
                if current_node in ancestor_dictionary[x] and x not in visited:
                    edges.append(x)
            for edge in edges:
                queue.enqueue(current_path + [edge])

    return earliest_ancestor