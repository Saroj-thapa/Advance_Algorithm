"""In this problem, we are given a binary tree where each node represents a location. 
A service center can be placed at any node, and one service center can cover the node itself, 
its parent, and its immediate children. A node is considered covered if it has a service center on it 
or if it is adjacent to a node with a service center. The main objective is to ensure that all nodes 
in the tree are covered using the minimum number of service centers. 
This problem requires careful placement because placing a service center at one node affects the coverage of 
nearby nodes. Therefore, the goal is to make smart decisions so that no node is left uncovered while also avoiding 
unnecessary service centers."""

"""The problem is solved using a bottom-up approach with Depth First Search (DFS). 
The idea is to process the tree from the leaf nodes up to the root so that each node can make a decision 
based on the condition of its children. During traversal, each node is assigned one of three states: 
not covered, has a service center, or covered by a nearby service center. If any child of a n
ode is not covered, a service center is placed at the parent to ensure coverage. 
If a child already has a service center, the parent is considered covered. 
If both children are covered but do not have service centers, the parent remains not covered 
so that it can be handled by its own parent. After the DFS is complete, a final check is performed on the root node,
and if it is not covered, one additional service center is placed. 
This method ensures that service centers are added only when necessary, 
resulting in complete coverage with the minimum number of centers.
"""
from collections import deque

# TREE NODE 
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        # Each node stores a value
        self.val = val

        # Pointer to left child
        self.left = left

        # Pointer to right child
        self.right = right


# BUILD TREE (LEVEL ORDER)
def build_tree(arr):
    """
    This function builds a binary tree from level-order input.
    'None' or 'null' means that node does not exist.
    """

    # If input list is empty or root itself is null, tree does not exist
    if not arr or arr[0] is None:
        return None

    # Create the root node using the first value
    root = TreeNode(arr[0])

    # Queue helps us attach children level by level
    queue = deque([root])

    # Index to move through input array
    i = 1

    # Continue until queue is empty or input is finished
    while queue and i < len(arr):
        # Take one node from the front of the queue
        node = queue.popleft()

        # -------- LEFT CHILD --------
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])   # create left child
            queue.append(node.left)        # add left child to queue
        i += 1

        # -------- RIGHT CHILD --------
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])  # create right child
            queue.append(node.right)       # add right child to queue
        i += 1

    # Return the built tree
    return root


#  SERVICE CENTER STATES 
# We use numbers to represent the condition of each node

NOT_COVERED = 0   # Node is NOT protected by any service center
HAS_CENTER  = 1   # Node HAS a service center installed on it
COVERED     = 2   # Node is protected but does NOT have a center


#  MAIN LOGIC 
def min_service_centers(root):
    """
    This function calculates the minimum number of service centers
    needed so that all nodes in the tree are covered.
    """

    centers = 0  # This will count total service centers used

    def dfs(node):
        """
        Depth First Search (post-order).
        Children are processed first, then parent.
        """
        nonlocal centers

        # If node is None, there is nothing to protect
        # So we treat it as already covered
        if node is None:
            return COVERED

        # Recursively check left and right children
        left_state = dfs(node.left)
        right_state = dfs(node.right)

        # CASE 1:
        # If any child is NOT covered,
        # we MUST place a service center here
        if left_state == NOT_COVERED or right_state == NOT_COVERED:
            centers += 1          # place a service center
            return HAS_CENTER    # current node now has a center

        # CASE 2:
        # If any child HAS a service center,
        # then current node is already covered
        if left_state == HAS_CENTER or right_state == HAS_CENTER:
            return COVERED

        # CASE 3:
        # Children are covered but none has a service center,
        # so this node is NOT covered
        return NOT_COVERED

    # Start DFS from the root
    root_state = dfs(root)

    # If root is still not covered,
    # we need to place one final service center at the root
    if root_state == NOT_COVERED:
        centers += 1

    # Return total number of service centers
    return centers


# ---------------- USER INPUT ----------------
print("Enter tree in level order (use 'null' for empty nodes)")
print("Example: 0 0 null 0 null 0 null null 0")

user_input = input("Input: ")

# Convert input into list of integers and None
arr = []
for x in user_input.replace(",", " ").split():
    if x.lower() == "null":
        arr.append(None)
    else:
        arr.append(int(x))

# Build the tree
root = build_tree(arr)

# Calculate minimum service centers
result = min_service_centers(root)

# Print final answer
print("\nMinimum number of service centers required:", result)

"""output 
Enter tree in level order (use 'null' for empty nodes)
Example: 0 0 null 0 null 0 null null 0
Input: 0 0 0 null 0 0 null 0 null 0 null 0 0 0

Minimum number of service centers required: 3
"""