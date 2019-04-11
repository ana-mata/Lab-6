#   Author: Ana Luisa Mata Sanchez
#   Course: CS2302
#   Assignment: Lab #6
#   Instructor: Olac Fuentes
#   Description: Program to draw mazes using dsf 
#   T.A.: Anindita Nath, Maliheh Zargaran
#   Last modified: 04/11/2019
#   Purpose: To compare time differences between compressed and non-compressed disjoint set forest

import matplotlib.pyplot as plt
import numpy as np
import random
import time

###################################### Code provided and written by Dr. Fuentes ######################################
def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
        
def dsfToSetList(S):
    #Returns aa list containing the sets encoded in S
    sets = [ [] for i in range(len(S)) ]
    for i in range(len(S)):
        sets[find(S,i)].append(i)
    sets = [x for x in sets if x != []]
    return sets

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r

def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri

def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri
         
def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri

def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

###################################### MY CODE ######################################

#Method that removes walls and creates the dsf using the standard union and find methods
def create_standard_dsf_maze(S,walls):
    #If there is only one set it means that all cells are reacheable from any cell
    while len(dsfToSetList(S))>1:
        #Finds a wall to remove
        d = random.randint(0,len(walls)-1)
        #If the elements that share a wall are not in the same set, remove it
        if find(S,walls[d][0]) != find(S,walls[d][1]):
            #make the elements belong to the same set
            union(S,walls[d][0],walls[d][1])
            #remove the wall
            walls.pop(d)

#Method that removes walls and creates the dsf using the union by size and compressed find methods
def create_compressed_dsf_maze(SC,wallsC):
    #If there is only one set it means that all cells are reacheable from any cell    
    while len(dsfToSetList(SC))>1:
        #Finds a wall to remove
        dC = random.randint(0,len(wallsC)-1)
        #If the elements that share a wall are not in the same set, remove it
        if find_c(SC,wallsC[dC][0]) != find_c(SC,wallsC[dC][1]):
            #make the elements belong to the same set
            union_by_size(SC,wallsC[dC][0],wallsC[dC][1])
            #remove the wall
            wallsC.pop(dC)
        
plt.close("all") 
maze_rows = 10
maze_cols = 15

#wall list & dsf for standard method
walls = wall_list(maze_rows,maze_cols)
S = DisjointSetForest(maze_rows*maze_cols)

#wall list & dsf for compressed method
wallsC = wall_list(maze_rows,maze_cols)
SC = DisjointSetForest(maze_rows*maze_cols)

#draw initial maze
draw_maze(walls,maze_rows,maze_cols,cell_nums=True)

print("######## Maze using standard find and union ########\n")

iStandardMazeT = time.time()
create_standard_dsf_maze(S,walls)        
fStandardMazeT = time.time()
draw_maze(walls,maze_rows,maze_cols) 

print("Time it took to create the maze:", fStandardMazeT-iStandardMazeT)
print("Maze row size:", maze_rows)
print("Maze column size:", maze_cols)

print("\n######## Maze using compressed find and union by size ########\n")

iCompressedMazeT = time.time()
create_compressed_dsf_maze(SC,wallsC)        
fCompressedMazeT = time.time()
draw_maze(wallsC,maze_rows,maze_cols) 

print("Time it took to create the maze:", fCompressedMazeT-iCompressedMazeT)
print("Maze row size:", maze_rows)
print("Maze column size:", maze_cols)
