#by 6n0m0n, SpaceSheep, and malachite_sprite

import copy as copy
import math

def LS_scaredypath(start_loc, finished_loc, session, avoid_arr, avoid_weights):
    finding_path = True
    root_path = path([start_loc], 1, "alive")
    paths = [root_path]
    visited_squares = []
    dir_try = [[0,1,0],[0,0,1],[0,-1,0],[0,0,-1]]
    weights_arr = copy.deepcopy(session.movetry_arr)

    for i in range(len(weights_arr)):
        for j in range(len(weights_arr[i])):
            for k in range(len(weights_arr[i][j])):
                weights_arr[i][j][k] = 1

    for i in range(len(weights_arr)):
        for j in range(len(weights_arr[i])):
            for k in range(len(weights_arr[i][j])):
                for w in range(len(avoid_arr)):
                    if distance([i,j,k], avoid_arr[w])<avoid_weights[w]:
                        weights_arr[i][j][k] = weights_arr[i][j][k] + avoid_weights[w] - distance([i,j,k], avoid_arr[w])

    while finding_path:
        for p in paths:

            p.timer = p.timer - 1

            if p.timer == 0:
                for d in dir_try:
                    cur_square = [p.list[-1][0]+d[0], p.list[-1][1]+d[1], p.list[-1][2]+d[2]]
                    pathblocker = session.map_arr[cur_square[0]][cur_square[1]][cur_square[2]].pathblocker
                    visited = cur_square in visited_squares

                    if not(pathblocker or visited):
                        new_path = path(p.list.append(cur_square), weights_arr[cur_square[0]][cur_square[1]][cur_square[2]], "alive")
                        paths.append(new_path)

                    if cur_square == finished_loc:
                        return p.list.append(cur_square)
                    
                p.status = "dead"

        paths = [p for p in paths if p.status == "alive"]

def path(square_list, timer, status):
    self.list = square_list
    self.timer = timer
    self.status = status

def distance(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])
