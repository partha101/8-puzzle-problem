import heap # imported heapq for implementing the queue of the search algorithm
import copy # imported copy in order to copy nodes used in the expand node functionality
import enum from Enum # imported enum datatype to enumerate over the algorithms

class Algorithm(Enum):
    UNIFORM_COST_SEARCH = 1
    MISPLACED_TILE_HEURISTIC = 2
    MANHATTAN_DISTANCE_HEAURISTIC = 3



# Creating the node class for storing evolving configurations of the puzzle
# This will be helpful in creating the tree structure for the problem
class Node:
    def __init__(self, state, parent, operator, depth, cost):
        self.state = state # this variable stores the configuration of the node. eg. [[1,2,3],...,[7,8,0]]
        self.parent = parent # this variable stores the parent node of a node
        self.operator = operator # this variable stores which operator was applied to the parent to get this node. eg. up, down, left or right
        self.depth = depth # this variable stores the depth of the node in the search tree from the root
        self.cost = cost # this variable stores the cost of the node. It will consist of depth of the node and heursitic value

    # we add the following dunder in order to specify heapq the node with the lowest cost to pop
    # in case two nodes have same cost, the node inserted first will be be popped from the heapq
    def __lt__(self, other):
        return self.cost < other.cost 
    

# adding a utility function to check if given configuration is solvable
def is_solvable(puzzle):
    # first we conver the puzzle into one dimensional array
    1D_puzzle = [ element for subproblem in puzzle for element in subproblem ]
    inversions = 0
    
    # simple for loop to iterate through pairs of elements in the flattened puzzle
    # and count the number of inversions
    for i in range(len(1D_puzzle)-1):
        for j in range (i+1, len(1D_puzzle)):
            if 1D_puzzle[i] != 0 and 1D_puzzle[j] != 0 and 1D_puzzle[i] > 1D_puzzle[j]:
                inversions+=1
    
    # checking if the puzzle is solvable
    # if no. of inversions is even the problem is solvable
    # else it's unsolvable
    return inversions % 2 == 0


# adding the function to get expand a for a given problem according to the
# general-search algorithm. 
def EXPAND(node):
    # First we find the position of the blank in the grid
    row, col = 0, 0
    for r in range(len(node.state)):
        if 0 in node.state[r]:
            row = r
            col = node.state[r].index(0)
            break
    
    # adding the list to store the children of a node
    children = []
    operators = [("up", -1, 0), ("down", 1, 0), ("left", 0, -1), ("right", 0, 1)]

    for op, dr, dc in operators:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(node.state) and 0 <= new_col < len(node.state[0]): # here we are checking if the resultant node index falls in the valid range
            new_state = copy.deepcopy(node.state) # creating a new node like the original node
            new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col] # swapping the blank with the neighbor 
            new_node = Node(new_state, node, op, node.depth + 1, 0) # increment the depth of the new node
            chidren.append(new_node) # appending the new node to the list of children

    return children # returning the array of children after expanding

# adding a function to print the puzzle
def print_puzzle(puzzle):
    for subarray in puzzle:
        print(subarray)
    print()


# Now we are going to define the cost functions for different heuristics
def cost_function(puzzle, goal, algorithm):
    cost = 0
    if (algorithm == Algorithm.MISPLACED_TILE_HEURISTIC):
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i]):
                if puzzle[i][j] != 0: 
                    cost += int(puzzle[i][j] == goal[i][j]) # checking the misplaced tile numbers
    
    elif (algorithm == Algorithm.MANHATTAN_DISTANCE_HEURISTIC):
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] != 0:
                    target_row, target_col = divmod(puzzle[i][j] - 1, len(puzzle))
                    cost += abs(i-target_row) + abs(j-target_col)
    return cost


# Now we are going to define the general search algorithm
def general_search(puzzle, goal, algorithm):
    initial_node = Node(puzzle, None, None, 0, 0)
    queue = [initial_node]
    nodes_expanded = 0
    max_queue_size = 0

    # till the queue is not empty 
    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        node = heapq.heappop(queue)
        if node.state == goal:
            return node, nodes_expanded, max_queue_size
        children = EXPAND(node)
        
        for child in children:
           child.cost = child.depth + cost_function(child.state, goal, algorithm) # here we are calculating f(n) = g(n) + h(n)
    return None, nodes_expanded, max_queue_size # in case we don't find a solution


# defining a function to print the solution

def print_solution(node, nodes_expanded, max_queue_size):
    path = []
    while node is not None:
        path.append(node)
        node = node.parent

    path.reverse()

    for step, node in enumerate(path):
        if node.operator is not None:
            print(f"The best state to expand with a g(n) = {node.depth} and h(n) = {node.cost - node.depth} is...")
        else:
            print("The best state to expand with a g(n) = 0 and h(n) =", node.cost, "is...")

     print("Goal state!")
     print("Solution depth was", path[-1].depth)
     print("Number of nodes expanded:", nodes_expanded)
     print("Max queue size:", max_queue_size)





