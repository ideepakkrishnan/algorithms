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

    def get_minimum(self):
        y = self
        x = self
        min = x.get_key()

        while x is not None:
            if x.get_key() < min:
                min = x.get_key()
                y = x
            x = x.get_sibling()
        return y

    def get_node(self, key):
        temp = self
        node = None
        while temp is not None:
            if temp.get_key() == key:
                node = temp
                break
            if temp.get_child() is None:
                temp = temp.get_sibling()
            else:
                node = temp.get_child().get_node(key)
                if node is None:
                    temp = temp.get_sibling()
                else:
                    break
        return node

    def reverse(self, s):
        rev = None
        if self.get_sibling() is not None:
            rev = self.get_sibling().reverse(self)
        else:
            rev = self
        self.set_sibling(s)
        return rev

    def walk(self, depth):
        result = ""
        for i in range(0, self.get_degree()):
            result += "  "

        result += ("key = " + str(self.get_key()) + ", degree = " + str(self.get_degree()) + "\n")

        x = self.get_child()
        while x is not None:
            result += x.walk(depth + 1)
            x = x.sibling

        return result

    def search_key(self, key):
        temp = self
        node = None
        while temp is not None:
            if temp.get_key() == key:
                node = temp
                break
            if temp.get_child() is None:
                temp = temp.get_sibling()
            else:
                node = temp.get_child().search_key(key)
                if node is None:
                    temp = temp.sibling
                else:
                    break
        return node

    def __init__(self, key):
        self.key = key
        self.parent = None
        self.degree = 0
        self.sibling = None
        self.child = None


# CLASS: BinomialHeap
# DESCRIPTION: BinomialHeap class stores the skeleton of binomial heap structure. It is initialized by specifying the
# root element of the binary heap structure as the default hollow element. Since the root is not null, we need to update
# the key and pointers stored in this element to point to the correct values.
class BinomialHeap(object):
    def __init__(self):
        self.head_node = None  # Initialize with head element which is None

    # FUNCTION SIGNATURE: get_head()
    # DESCRIPTION: This function fetches the head of this binomial heap and returns it to the caller
    # ARGUMENTS: -NA-
    # RETURNS: A Node object which is the head of this binomial heap
    def get_head(self):
        return self.head_node

    def set_head(self, newHead):
        self.head_node = newHead

    # FUNCTION SIGNATURE: binomial_heap_minimum()
    # DESCRIPTION: Since a binomial heap is min-heap-ordered, the minimum key must reside in a root node. This
    # procedure checks all roots, which number at most [lg n] + 1, saving the current minimum in minNodeKey and a
    # pointer to the current minimum in minNode.
    # ARGUMENTS: -NA-
    # RETURNS: A Node object which stores the minimum value within the binomial heap
    def binomial_heap_minimum(self):
        minNode = self.get_head()
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
        return y, z

    # FUNCTION SIGNATURE: binomial_heap_merge(BinomialHeap)
    # DESCRIPTION: This function merges the heap passed in as argument with this instance of binomial heap
    # ARGUMENTS:
    #  node2 - A Node object which is to be merged with this heap
    # RETURNS: The new head Node for the merged binomial heaps
    def binomial_heap_merge(self, node2):
        node1 = self.get_head()
        while node1 is not None and node2 is not None:
            if node1.get_degree() == node2.get_degree():
                tempNode = node2
                node2 = node2.get_sibling()
                tempNode.set_sibling(node1.get_sibling())
                node1.set_sibling(tempNode)
                node1 = tempNode.get_sibling()
            else:
                if node1.get_degree() < node2.get_degree():
                    if node1.get_sibling() is None or node1.get_sibling().get_degree() > node2.get_degree():
                        tempNode = node2
                        node2 = node2.get_sibling()
                        tempNode.set_sibling(node1.get_sibling())
                        node1.set_sibling(tempNode)
                        node1 = tempNode.get_sibling()
                    else:
                        node1 = node1.get_sibling()
                else:
                    tempNode = node1
                    node1 = node2
                    node2 = node2.get_sibling()
                    node1.set_sibling(tempNode)
                    if tempNode == self.get_head():
                        self.set_head(node1)

        if node1 is None:
            node1 = self.get_head()
            while node1.get_sibling() is not None:
                node1 = node1.get_sibling()
            node1.set_sibling(node2)

    # FUNCTION SIGNATURE: binomial_heap_union(Node)
    # DESCRIPTION: The following functions unites the node passed in as arguments and returns the resulting heap
    # ARGUMENTS:
    #  h2 - A BinomialHeap object to be merged with this instance of binomial heap
    # RETURNS: A BinomialHeap object which is a union of the two objects passed in as arguments
    def binomial_heap_union(self, node2):
        self.binomial_heap_merge(node2)

        prevTemp = None
        temp = self.get_head()
        nextTemp = self.get_head().get_sibling()

        while nextTemp is not None:
            if (temp.get_degree() != nextTemp.get_degree()) or (nextTemp.get_sibling() is not None and nextTemp.get_sibling().get_degree() == temp.get_degree()):
                prevTemp = temp
                temp = nextTemp
            else:
                if temp.get_key() <= nextTemp.get_key():
                    temp.set_sibling(nextTemp.get_sibling())
                    nextTemp.set_parent(temp)
                    nextTemp.set_sibling(temp.get_child())
                    temp.set_child(nextTemp)
                    temp.set_degree(temp.get_degree() + 1)
                else:
                    if prevTemp is None:
                        self.set_head(nextTemp)
                    else:
                        prevTemp.set_sibling(nextTemp)
                    temp.set_parent(nextTemp)
                    temp.set_sibling(nextTemp.get_child())
                    nextTemp.set_child(temp)
                    nextTemp.set_degree(nextTemp.get_degree() + 1)
                    temp = nextTemp
            nextTemp = temp.get_sibling()

    # FUNCTION SIGNATURE: binomial_heap_extract_min()
    # DESCRIPTION: This function finds the minimum value from the binomial heap and removes the its Node from the heap
    # ARGUMENTS: -NA-
    # RETURNS: A Node object which stores the minimum value in the Heap
    def binomial_heap_extract_min(self):
        temp = self.get_head()
        prevTemp = None
        minNode = self.get_head().get_minimum()
        while temp.get_key() != minNode.get_key():
            prevTemp = temp
            temp = temp.get_sibling()

        if prevTemp is None:
            self.set_head(temp.get_sibling())
        else:
            prevTemp.set_sibling(temp.get_sibling())

        temp = temp.get_child()
        fakeNode = temp
        while temp is not None:
            temp.set_parent(None)
            temp = temp.get_sibling()

        if not(self.get_head() is None and fakeNode is None):
            if self.get_head() is None and fakeNode is not None:
                self.set_head(fakeNode.reverse(None))
            else:
                if not(Node is not None and fakeNode is None):
                    self.binomial_heap_union(fakeNode.reverse(None))

        return minNode.get_key()

    # FUNCTION SIGNATURE: binomial_heap_insert(Node)
    # DESCRIPTION: The following function inserts a new node into the binomial heap by creating a one node binomial
    # heap and merging it with this instance of binomial heap
    # ARGUMENTS:
    #  x - A Node object which needs to be inserted into the binomial heap
    # RETURNS: True iff the procedure is completed successfully
    def binomial_heap_insert(self, x):
        if self.get_head() is None:
            self.set_head(x)
            return self
        else:
            return self.binomial_heap_union(x)

    # FUNCTION SIGNATURE: binomial_heap_extract_min()
    # DESCRIPTION: This function decreases the node x in this instance of binomial heap to a new value k
    # ARGUMENTS:
    #  x - The Node whose value is to be updated
    #  k - new value for the node
    # RETURNS: true iff the value is updated, false iff the value of k is greater than the current key in Node x
    def binomial_heap_decrease_key(self, val, k):
        temp = self.get_head().get_node(val)
        if temp is None:
            return False
        temp.set_key(k)
        tempParent = temp.get_parent()

        while tempParent is not None and temp.get_key() < temp.get_parent().get_key():
            z = temp.get_key()
            temp.set_key(tempParent.get_key())
            tempParent.set_key(z)

            temp = tempParent
            tempParent = tempParent.get_parent()

    # FUNCTION SIGNATURE: binomial_heap_delete(Node)
    # DESCRIPTION: This function deletes a Node object from this instance os the binomial heap by decreasing the key
    #              stored in x to -9999 and then extracting this Node from the heap
    # ARGUMENTS:
    #  x - The Node object to be deleted from the heap
    # RETURNS: True iff the Node is deleted from the heap
    def binomial_heap_delete(self, x):
        self.binomial_heap_decrease_key(x, -9999)
        self.binomial_heap_extract_min()
        return True

    # FUNCTION SIGNATURE: binomial_heap_walk()
    # DESCRIPTION: This function prints the current structure of the binomial heap
    # ARGUMENTS: -NA-
    # RETURNS: -NA-
    def binomial_heap_walk(self):
        result = ""
        x = self.get_head()
        while x is not None:
            result += x.walk(0)
            x = x.get_sibling()
        print result


    def binomial_node_search(self, key):
        currNode = self.get_head()
        if currNode.get_key() == key:
            return currNode
        else:
            return currNode.search_key(key)


# FUNCTION SIGNATURE: make_binomial_heap()
# DESCRIPTION: This function creates a new Binary Heap object and returns the object and its head node to the caller.
# ARGUMENTS: -NA-
# RETURNS: A BinaryHeap object and a Node object which points to the head of this Binary Heap
def make_binomial_heap():
    heapObj = BinomialHeap()
    return heapObj


# FUNCTION SIGNATURE: main()
# DESCRIPTION: This function acts as the starting point for this program. All the initial declarations and program
# logic go in here
# ARGUMENTS: -NA-
# RETURNS: -NA-
def main():
    # Creating a test heap
    heap1 = make_binomial_heap()

    # Insert procedures for heap1
    heap1.binomial_heap_insert(Node(37))
    heap1.binomial_heap_insert(Node(41))
    print "Initializing Heap 1:"
    heap1.binomial_heap_walk()

    # Creating another test heap
    heap2 = make_binomial_heap()

    # Insert operations for heap2
    heap2.binomial_heap_insert(Node(10))
    heap2.binomial_heap_insert(Node(28))
    heap2.binomial_heap_insert(Node(77))
    heap2.binomial_heap_insert(Node(13))
    print "Initializing Heap 2:"
    heap2.binomial_heap_walk()

    # Union of both heaps
    heap1.binomial_heap_union(heap2.get_head())
    print "Union of heap 1 and heap 2:"
    heap1.binomial_heap_walk()

    # Creating another test heap
    heap3 = make_binomial_heap()
    heap3.binomial_heap_insert(Node(1))
    heap3.binomial_heap_insert(Node(6))
    heap3.binomial_heap_insert(Node(16))
    heap3.binomial_heap_insert(Node(12))
    heap3.binomial_heap_insert(Node(25))
    heap3.binomial_heap_insert(Node(8))
    heap3.binomial_heap_insert(Node(14))
    heap3.binomial_heap_insert(Node(29))
    heap3.binomial_heap_insert(Node(26))
    heap3.binomial_heap_insert(Node(23))
    heap3.binomial_heap_insert(Node(18))
    heap3.binomial_heap_insert(Node(11))
    heap3.binomial_heap_insert(Node(17))
    heap3.binomial_heap_insert(Node(38))
    heap3.binomial_heap_insert(Node(42))
    heap3.binomial_heap_insert(Node(27))

    print "Initializing heap 3:"
    heap3.binomial_heap_walk()

    # Union of heap 3 with heap 1
    heap1.binomial_heap_union(heap3.get_head())
    print "Union of heap 1 and heap 3:"
    heap1.binomial_heap_walk()

    # Minimum value in heap 1
    print "Minimum value in heap 1: ", str(heap1.binomial_heap_minimum().get_key())

    # Extract min from heap 1
    print "Extracted minimum value from heap 1: ", str(heap1.binomial_heap_extract_min())
    print "Heap after first extract min:"
    heap1.binomial_heap_walk()

    # Extract min from heap 1
    print "Extracted minimum value from heap 1: ", str(heap1.binomial_heap_extract_min())
    print "Heap after second extract min:"
    heap1.binomial_heap_walk()

    # Decrease key in heap 1
    heap1.binomial_heap_decrease_key(42, 19)
    print "Heap after decrease key:"
    heap1.binomial_heap_walk()

    # Deleting key from heap
    heap1.binomial_heap_delete(heap1.binomial_node_search(8))
    print "Heap after delete:"
    heap1.binomial_heap_walk()


if __name__ == "__main__":
    main()