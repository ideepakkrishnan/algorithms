# ---------------------------------------------------------------
# CLASSES
# ---------------------------------------------------------------


# The class which defines the node object which stores the info
# regarding the each node in the linked list. To elaborate a bit
# more, each node object stores the value and a pointer towards
# the next node in a linked list
class node:

    def get_val(self):
        return self.val

    def get_nxt(self):
        return self.nxt

    # Class initializer
    def __init__(self, val = -1, nxt = None):
        self.val = val  # Store the value for this node
        self.nxt = nxt  # Pointer to the next node in list

# ---------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------


# This function formats the output for the user once the lists
# have been processed and we have a result
def print_result(testCase, intersectionPoint):
    if intersectionPoint is None:
        print testCase + ": The linked lists do not intersect"
    else:
        print testCase + ": The point of intersection is: [" + \
              str(intersectionPoint.get_val()) + "]"


# This function finds the length of a linked list by traversing
# through it and returns the calculated length to the caller.
def find_length(currNode):
    length = 0
    # The end of a linked list is denoted by a node which has -1
    # as its value. Traverse through till this node is found to
    # find the length.
    while currNode.get_val() != -1:
        length += 1
        currNode = currNode.get_nxt()
    return length


# Move forward in a linked list by the number of steps specified
# in the argument
def move_forward(currNode, steps):
    while steps > 0:
        currNode = currNode.get_nxt()
        steps -= 1
    return currNode


# This function takes in the starting point of two linked lists
# A and B. Then it traverses through the lists to find out the
# point of intersection for these two lists.
def find_intersection(currNodeInA, currNodeInB):

    # Local variables to store the length of both linked lists
    lenA = find_length(currNodeInA)
    print "Length of linked list A: " + str(lenA)
    lenB = find_length(currNodeInB)
    print "Length of linked list B: " + str(lenB)

    # Find the difference in length between the two linked
    # lists and store it so that we can use it to step forward
    # in the longer linked list before doing a one-to-one
    # comparison
    lenDiff = lenA - lenB
    if lenDiff < 0:
        lenDiff = -lenDiff
    print "Difference in lengths: " + str(lenDiff)

    # Move forward by lenDiff in the longer linked list
    if lenA > lenB:
        currNodeInA = move_forward(currNodeInA, lenDiff)
        print "Linked list A is longer. Moved forward to [" \
              + str(currNodeInA.get_val()) + "]"
    elif lenB > lenA:
        currNodeInB = move_forward(currNodeInB, lenDiff)
        print "Linked list B is longer. Moved forward to [" \
              + str(currNodeInA.get_val()) + "]"
    else:
        print "Both linked lists are of equal length"

    # Do a one-to-one comparison between the elements of both
    # the linked lists to find the point where they intersect
    while currNodeInA.get_val() != -1:
        if currNodeInA == currNodeInB:
            return currNodeInA
        else:
            currNodeInA = currNodeInA.get_nxt()
            currNodeInB = currNodeInB.get_nxt()

    # No intersection between the two lists
    return None


# ---------------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------------
def main():
    try:
        endNone = node()
        node1 = node(1, endNone)
        node2 = node(2, node1)
        node3 = node(3, node2)
        node4 = node(4, node3)
        node5 = node(5, node4)
        node6 = node(6, node5)
        node7 = node(7, node4)
        node8 = node(8, node7)
        node9 = node(9, node8)
        node10 = node(10, node9)

        endNode2 = node()
        node11 = node(11, endNode2)
        node12 = node(12, node11)
        node13 = node(13, node12)
        node14 = node(14, node13)
        node15 = node(15, node14)
        node16 = node(16, node15)

        endNode3 = node()
        endNode4 = node()

        # Test Case 1: Intersecting lists of different lengths
        # [10] -> [9] -> [8] -> [7]
        #                        |
        #                       [4] -> [3] -> [2] -> [1]
        #                        |
        #                [6] -> [5]

        intersectionPoint = find_intersection(node10, node6)
        print_result("TC1", intersectionPoint)

        # Test Case 2: Intersecting lists of equal lengths
        # [8] -> [7]
        #         |
        #        [4] -> [3] -> [2] -> [1]
        #         |
        # [6] -> [5]

        intersectionPoint = find_intersection(node8, node6)
        print_result("TC2", intersectionPoint)

        # Test Case 3: Non-intersecting lists of same lengths
        # [6] -> [5] -> [4] -> [3] -> [2] -> [1]
        # [16] -> [15] -> [14] -> [13] -> [12] -> [11]

        intersectionPoint = find_intersection(node16, node6)
        print_result("TC3", intersectionPoint)

        # Test Case 4: Non-intersecting lists of diff lengths
        # [6] -> [5] -> [4] -> [3] -> [2] -> [1]
        # [13] -> [12] -> [11]

        intersectionPoint = find_intersection(node6, node13)
        print_result("TC4", intersectionPoint)

        # Test case 5: One of the lists is empty
        # [6] -> [5] -> [4] -> [3] -> [2] -> [1]
        # empty list

        intersectionPoint = find_intersection(node6, endNode3)
        print_result("TC5", intersectionPoint)

        # Test case 6: Both the lists are empty
        intersectionPoint = find_intersection(endNode4, endNode3)
        print_result("TC6", intersectionPoint)
    except Exception as e:
        print "An unexpected error occurred: " + e.message

if __name__ == "__main__":
    main()