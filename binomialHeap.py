# ---------------------------------------------------------------
# OVERVIEW
# ---------------------------------------------------------------
# The following script implements a binomial heap in Python. A binary heap is a collection of binomial trees.
# A Binomial Tree of order k has following properties.
# a) It has exactly 2k nodes.
# b) It has depth as k.
# c) There are exactly kCi nodes at depth i for i = 0, 1, . . . , k.
# d) The root has degree k and children of root are Binomial Trees with order k-1, k-2,.. 0 from left to right
#
# eg. A Binomial Heap with 13 nodes:
#
# 12------------10--------------------20
#              /  \                 /  | \
#            15    50             70  50  40
#            |                  / |    |
#            30               80  85  65
#                             |
#                            100
#
# It is a collection of 3 Binomial Trees of orders 0, 2 and 3 from left to right.


# ---------------------------------------------------------------
# CLASSES
# ---------------------------------------------------------------


# CLASS: Node
# DESCRIPTION: This class stores the object representation of each node. Each node gets initialized with the following
# fields along with their getters and setters:
# ---------------------------------------------------------
# [Element Name] -> [Initialization value] >> [Description]
# ---------------------------------------------------------
# parent -> None >> Parent of this node
# key -> None >> The value stored at this node
# degree -> -1 >> Height of the node
# sibling -> None >> Points to the adjacent sibling on the right of this element
# child -> None >> Stores a pointer to the left-most child of this node
class Node:
    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = key

    def get_degree(self):
        return self.degree

    def set_degree(self, degree):
        self.degree = degree

    def get_sibling(self):
        return self.sibling

    def set_sibling(self, sibling):
        self.sibling = sibling

    def get_child(self):
        return self.child

    def set_child(self, child):
        self.child = child

    def __init__(self, key):
        self.key = key
        self.parent = None
        self.degree = -1
        self.sibling = None
        self.child = None


# CLASS: BinomialHeap
# DESCRIPTION: BinomialHeap class stores the skeleton of binomial heap structure. It is initialized by specifying the
# root element of the binary heap structure as the default hollow element. Since the root is not null, we need to update
# the key and pointers stored in this element to point to the correct values.
class BinomialHeap(object):
    def __init__(self, createNode=Node):
        self.nil = createNode(None)  # Initialize an empty placeholder node to mark all null pointers
        self.create_node = createNode  # Function to create a placeholder for each Node
        self.root_list = [self.nil]  # Initialize with head element which is None

    # FUNCTION SIGNATURE: get_head()
    # DESCRIPTION: This function fetches the head of this binomial heap and returns it to the caller
    # ARGUMENTS: -NA-
    # RETURNS: A Node object which is the head of this binomial heap
    def get_head(self):
        return self.root_list[0]

    def set_head(self, newHead):
        self.root_list[0] = newHead

    # FUNCTION SIGNATURE: binomial_heap_minimum()
    # DESCRIPTION: Since a binomial heap is min-heap-ordered, the minimum key must reside in a root node. This
    # procedure checks all roots, which number at most [lg n] + 1, saving the current minimum in minNodeKey and a
    # pointer to the current minimum in minNode.
    # ARGUMENTS: -NA-
    # RETURNS: A Node object which stores the minimum value within the binomial heap
    def binomial_heap_minimum(self):
        minNode = self.get_head().get_sibling()
        minNodeKey = 9999
        if minNode is not None:
            currNode = minNode.get_sibling()
            while currNode is not None:
                nodeKey = currNode.get_key()
                if nodeKey < minNodeKey:
                    minNode = currNode
                    minNodeKey = nodeKey
                currNode = currNode.get_sibling()
        return minNode

    # FUNCTION SIGNATURE: binomial_link(Node, Node)
    # DESCRIPTION: This function makes the Node y parent of Node z
    # ARGUMENTS:
    #  y - A Node object whose parent is to be altered
    #  z - A Node object which acts as the new parent for Node y
    # RETURNS: True iff the procedure is completed successfully
    def binomial_link(self, y, z):
        y.set_parent(z)
        y.set_sibling(z.get_child())
        z.set_child(y)
        z.set_degree(z.get_degree() + 1)
        return True

    # FUNCTION SIGNATURE: binomial_heap_union(BinomialHeap, BinomialHeap)
    # DESCRIPTION: The following functions unites two heaps passed in as arguments and returns the resulting heap
    # ARGUMENTS:
    #  h1 - A BinomialHeap object which needs to be merged with h2
    #  h2 - A BinomialHeap object to be merged with h1
    # RETURNS: A BinomialHeap object which is a union of the two objects passed in as arguments
    def binomial_heap_union(self, h1, h2):
        heap, head = make_binomial_heap()
        heap.set_head(self.binomial_heap_merge(h1, h2))

        if heap.get_head() == self.nil:
            return heap

        prev_x = self.nil
        x = heap.get_head()
        next_x = x.get_sibling()

        while next_x != self.nil:
            if ((x.get_degree() != next_x.get_degree()) or
                ((next_x.get_sibling() is not self.nil) and
                     (next_x.get_sibling().get_degree() == x.get_degree()))):
                prev_x = x
                x = next_x
            elif x.get_key() <= next_x.get_key():
                x.set_sibling(next_x.get_sibling())
                self.binomial_link(x, next_x)
                x = next_x
            next_x = x.get_sibling()

        return heap

    # FUNCTION SIGNATURE: binomial_heap_insert(Node)
    # DESCRIPTION: The following function inserts a new node into the binomial heap
    # ARGUMENTS:
    #  x - A Node object which needs to be inserted into the binomial heap
    # RETURNS: True iff the procedure is completed successfully
    def binomial_heap_insert(self, x):
        heap, head = make_binomial_heap()
        x.set_parent(self.nil)
        x.set_child(self.nil)
        x.set_sibling(self.nil)
        x.set_degree(0)
        heap.set_head(x)
        return self.binomial_heap_union(this, heap)

    # FUNCTION SIGNATURE:
    # DESCRIPTION:
    # ARGUMENTS:
    # RETURNS:
    def function_boiler_plate(self):
        return None


# FUNCTION SIGNATURE: make_binomial_heap()
# DESCRIPTION: This function creates a new Binary Heap object and returns the object and its head node to the caller.
# ARGUMENTS: -NA-
# RETURNS: A BinaryHeap object and a Node object which points to the head of this Binary Heap
def make_binomial_heap():
    heapObj = BinomialHeap()
    return heapObj, heapObj.get_head()
