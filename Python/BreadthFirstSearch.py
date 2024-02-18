tree = {
    'A': {'B', 'C'},
    'B': {'D', 'E'},
    'C': {'F', 'G'},
    'D': {'H'},
    'E': {None},
    'F': {None},
    'G': {'I'},
}

goal_node = 'F'
first_node = 'A'
active_node = first_node

open = [first_node]
close = []

def movegen(current_node):
    global active_node
    close.insert(0, current_node)
    open.pop(0) #pop first node in the open list

    # Explore children
    if current_node not in open or close or current_node in tree:
        open.extend(tree[current_node])
        active_node = open[len(open)-1] #set active node as last node in open list

def Goal_test(current_node, target_node):
    if current_node == target_node:
        close.insert(0,current_node) #add current node as last node in the sequence
        print("GOAL FOUND")
    else:
        movegen(current_node)

# Perform BFS search
while open and goal_node in tree:
    if goal_node in close:
        break  # Exit the loop when the goal is found

    Goal_test(open[0], goal_node)


close.reverse()
if close:
    print("Search Sequence:", close)
else:
    print("Goal Dosen't exist")