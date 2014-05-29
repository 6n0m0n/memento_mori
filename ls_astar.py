#by 6n0m0n, SpaceSheep, and malachite_sprite

class Tree(object):
    def __init__(self, data):
        self.parent=None
        self.children=[]
        self.data=data
    
    def set_parent(self, parent):
        self.parent=parent
        self.parent.children.append(self) # I think this works?

    def __lt__(self, other):
        return self.data < other.data
    def __gt__(self, other):
        return self.data > other.data
    def __eq__(self, other):
        return self.data == other.data
    def __le__(self, other):
        return self.data <= other.data
    def __ge__(self, other):
        return self.data >= other.data
    def __ne__(self, other):
        return self.data != other.data

def next_location_in_path(char, start, finish, session):
    path=[]
    end_node=astar(char, start, finish, session)
    if end_node is None: return None
    parent=end_node.parent
    previous_node=None
    current_node=end_node
    while parent is not None:
        path.append(current_node.data)
        previous_node=current_node
        current_node=parent
        parent=current_node.parent
    print(path)
    return previous_node.data

def astar(char, start, finish, session):
    # a location is a list of coordinates; z, y, x.
    # a node is a Tree object that holds a location and references to the parent and children of that node
    
    # adjacent_locations holds a tuple containing the adjacent location and the node it is adjacent to
    
    root=Tree(start)
    visited_locations=[start]
    adjacent_tuples=get_adjacent_tuples(char, visited_locations, root, session, finish)
    current_node=root
    adjacent_tuples.sort()
    while len( adjacent_tuples ) > 0:
        if current_node.data == finish:
            return current_node
        visited_locations.append( current_node.data )
        adjacent_tuples.extend(get_adjacent_tuples(char, visited_locations, current_node, session, finish))
        # TODO: adjust adjacent_tuples for more effecient popLefts
        adjacent_tuples.sort()
        next_tuple=adjacent_tuples.pop(0)
        current_node=Tree(next_tuple[1])
        current_node.set_parent(next_tuple[2])
    return None

def get_adjacent_tuples(char, visited, current_node, session, dest):
    current_loc=current_node.data
    new_locations=[ [current_loc[0],current_loc[1]+1,current_loc[2]],
                    [current_loc[0],current_loc[1]-1,current_loc[2]],
                    [current_loc[0],current_loc[1],current_loc[2]+1],
                    [current_loc[0],current_loc[1],current_loc[2]-1]
                    ]
    locations_to_return=[]
    for location in new_locations:
        square=session.map_arr[location[0]][location[1]][location[2]]
        if (not square.pathblocker) and (location not in visited) and (square not in char.vision or square.contained_ch is None):
            weight=get_weight(location, dest)
            locations_to_return.append((weight, location, current_node))
    return locations_to_return

def get_weight(location, destination):
    return NY_dist(location, destination)

def NY_dist(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

        
