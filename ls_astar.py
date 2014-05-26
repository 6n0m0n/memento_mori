#by 6n0m0n, SpaceSheep, and malachite_sprite

class Tree(object):
    def __init__(self, data):
        self.parent=None
        self.children=[]
        self.data=data
    
    def set_parent(self, parent):
        self.parent=parent
        self.parent.children.append(self) # I think this works?

def next_location_in_path(start, finish, session):
    path=[]
    end_node=astar(start, finish, session)
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

def astar(start, finish, session):
    # a location is a list of coordinates; z, y, x.
    # a node is a Tree object that holds a location and references to the parent and children of that node
    
    # adjacent_locations holds a tuple containing the adjacent location and the node it is adjacent to
    
    root=Tree(start)
    visited_locations=[start]
    adjacent_tuples=get_adjacent_tuples(visited_locations, root, session)
    current_node=root
    while len( adjacent_tuples ) > 0:
        if current_node.data == finish:
            return current_node
        visited_locations.append( current_node.data )
        adjacent_tuples.extend(get_adjacent_tuples(visited_locations, current_node, session))
        # TODO: adjust adjacent_tuples for more effecient popLefts
        next_tuple=adjacent_tuples.pop(0)
        current_node=Tree(next_tuple[0])
        current_node.set_parent(next_tuple[1])
    return None

def get_adjacent_tuples(visited, current_node, session):
    current_loc=current_node.data
    new_locations=[ [current_loc[0],current_loc[1]+1,current_loc[2]],
                    [current_loc[0],current_loc[1]-1,current_loc[2]],
                    [current_loc[0],current_loc[1],current_loc[2]+1],
                    [current_loc[0],current_loc[1],current_loc[2]-1]
                    ]
    locations_to_return=[]
    for location in new_locations:
        square=session.map_arr[location[0]][location[1]][location[2]]
        if (not square.pathblocker) and (location not in visited):
            locations_to_return.append((location, current_node))
    return locations_to_return

        
