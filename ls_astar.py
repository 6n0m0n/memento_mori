#by 6n0m0n, SpaceSheep, and malachite_sprite

from collections import deque #deque has faster popleft than standard list

def next_point_in_path( start, dest, session ):
    return astar( start, dest, session )[1]
    #now, i think this is right. lesse...

def astar(start, dest, session): #yay, latin stars! Whoo!
    visited = []
    return rec_help( deque([ (0, [start]) ]), dest, session, visited) #also yay, recursion! Heh, also deque is funny.
                #N.B. unlike bfs, active is a deque (list) of tuples, where the first element is the 
                # weight of the following path, and the second element is a list of coordinates that
                # is the path itself.

def rec_help(active, dest, session, visited):
    if len(active) <= 0: return None #return None if there is no path (if there are no active squares)
    current_path = active.popleft()[1] #otherwise get the path to the current location
    current_loc = current_path[-1] #(current location is the one at the end of the path to it -- isn't the [-1] thing nifty?)
    if current_loc is dest: return current_path #yay! we're there! and it's been <10 lines in!
    visited.append( current_loc ) #awww, not done yet. Okay, finished with this location, mark it as visited
    new_active_list = active.extend(get_paths_to_surroundings_weights(current_path, visited, session, dest))
                #just as in bfs, extend the active paths list to contain all the surrounding locations
    return rec_help( sorted(new_active_list, dest), dest, session, visited)
                #Now, unlike before, sort the new active paths list baised on the end location's distance
                # to the destination


def get_paths_to_surroundings_weights(current_path, visited, session, dest):
    current_loc = current_path[-1] #gosh I love this trick...
    paths_weights = []   # WARNING!! Make sure this stuff below is right coord format with rest of 2M!
    new_coords = [  [current_loc[0],current_loc[1]+1,current_loc[2]], #each line ought to be a coordinate triple... I think.
                    [current_loc[0],current_loc[1]-1,current_loc[2]], #it's important to note that this is where adjacency is
                    [current_loc[0],current_loc[1],current_loc[2]+1], # decided -- as of now there's no way to go up or down
                    [current_loc[0],current_loc[1],current_loc[2]-1]  # a level. But that can change.
                ]
    for coord in new_coords: #this is a funky way of getting the square that corrisponds to a set of coordinates, in order to
        temp = session.map_arr[coord[0]][coord[1]][coord[2]] # see if it's passible / visited, 'cause we wouldn't want that.
        weight = NY_distance(coord, dest)
        if ( not(temp.pathblocker) or (temp.contained_ch is None) ) and (not(coord in visited)):
            paths_weights.append( (weight, current_path.append(coord)) )
    return paths_weights #then we return the paths to those coordinates next to the current one, to be put into the active paths deque. Yay!

def NY_distance(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

