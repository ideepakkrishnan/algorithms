# ---------------------------------------------------------------
# GLOBALS
# ---------------------------------------------------------------

RED = "red"
BLACK = "black"

# ---------------------------------------------------------------
# CLASSES
# ---------------------------------------------------------------


class node:
    def get_left(self):
        return self.left

    def set_left(self, newLeft):
        self.left = newLeft

    def get_right(self):
        return self.right

    def set_right(self, newRight):
        self.right = newRight

    def get_parent(self):
        return self.parent

    def set_parent(self, newParent):
        self.parent = newParent

    def get_color(self):
        return self.color

    def set_color(self, newColor):
        self.color = newColor

    def get_key(self):
        return self.key

    def set_key(self, newKey):
        self.key = newKey

    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = BLACK


class tree(object):
    def __init__(self, createNode=node):
        self.nil = createNode(None)  # T.nil
        self.root = self.nil
        self.create_node = createNode

    def sort(self, x=None):
        if x is None:
            x = self.root
        if x != self.nil:
            self.sort(x.get_left())
            print x.get_key()
            self.sort(x.get_right())

    def successor(self, key):
        x = self.search(key)
        if x.get_right() != self.nil:
            return self.min(x.get_right())
        y = x.get_parent()
        while y != self.nil and x == y.get_right():
            x = y
            y = y.get_parent()
        return y

    def predecessor(self, key):
        x = self.search(key)
        if x.get_left() != self.nil:
            return self.max(x.get_left())
        y = x.get_parent()
        while y != self.nil and x == y.get_left():
            x = y
            y = y.get_parent()
        return y

    def search(self, key, x=None):
        # x represents the root of the tree
        if x is None:
            x = self.root
        while x != self.nil and key != x.get_key():
            if key < x.get_key():
                x = x.get_left()
            else:
                x = x.get_right()
        return x

    def min(self, x=None):
        if x is None:
            x = self.root
        while x.get_left() != self.nil:
            x = x.get_left()
        return x

    def max(self, x=None):
        if x is None:
            x = self.root
        while x.get_right() != self.nil:
            x = x.get_right()
        return x

    def insert(self, key):
        self.insert_node(self.create_node(key))

    def insert_node(self, z):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.get_key() < x.get_key():
                x = x.get_left()
            else:
                x = x.get_right()
        z.set_parent(y)
        if y == self.nil:
            self.root = z
        elif z.get_key() < y.get_key():
            y.set_left(z)
        else:
            y.set_right(z)
        z.set_left(self.nil)
        z.set_right(self.nil)
        z.set_color(RED)
        self.insert_fixup(z)

    def insert_fixup(self, z):
        while z.get_parent().get_color() == RED:
            if z.get_parent() == z.get_parent().get_parent().get_left():
                y = z.get_parent().get_parent().get_right()
                if y.get_color() == RED:
                    z.get_parent().set_color(BLACK)
                    y.set_color(BLACK)
                    z.get_parent().get_parent().set_color(RED)
                    z = z.get_parent().get_parent()
                else:
                    if z == z.get_parent().get_right():
                        z = z.get_parent()
                        self.left_rotate(z)
                    z.get_parent().set_color(BLACK)
                    z.get_parent().get_parent().set_color(RED)
                    self.right_rotate(z.get_parent().get_parent())
            else:
                y = z.get_parent().get_parent().get_left()
                if y.get_color == RED:
                    z.get_parent().set_color(BLACK)
                    y.set_color(BLACK)
                    z.get_parent().get_parent().set_color(RED)
                    z = z.get_parent().get_parent()
                else:
                    if z == z.get_parent().get_left():
                        z = z.get_parent()
                        self.right_rotate(z)
                    z.get_parent().set_color(BLACK)
                    z.get_parent().get_parent().set_color(RED)
                    self.left_rotate(z.get_parent().get_parent())
        self.root.set_color(BLACK)

    def left_rotate(self, x):
        print "inside left rotate for: " + str(x.get_key())
        y = x.get_right()
        x.set_right(y.get_left())
        if y.get_left() != self.nil:
            y.get_left().set_parent(x)
        y.set_parent(x.get_parent())
        if x.get_parent() == self.nil:
            self.root = y
        elif x == x.get_parent().get_left():
            x.get_parent().set_left(y)
        else:
            x.get_parent().set_right(y)
        y.set_left(x)
        x.set_parent(y)

    def right_rotate(self, y):
        print "inside right rotate for: " + str(y.get_key())
        x = y.get_left()
        y.set_left(x.get_right())
        if x.get_right() != self.nil:
            x.get_right().set_parent(y)
        x.set_parent(y.get_parent())
        if y.get_parent() == self.nil:
            self.root = x
        elif y == y.get_parent().get_right():
            y.get_parent().set_right(x)
        else:
            y.get_parent().set_left(x)
        x.set_right(y)
        y.set_parent(x)

    def is_valid_rb_node(self, node):
        # Check 1: Node should have two children
        if (node.get_left() and not node.get_right()) or (node.get_right() and not node.get_left()):
                return 0, False

        # Check 2: Leaves should be black
        if not node.get_left() and not node.get_right() and node.get_color() == RED:
            return 0, False

        # Check 3: if node is red, children should be black
        if node.get_color() == RED and node.get_left() and node.get_right():
            if node.get_left().get_color() == RED or node.get_right().get_color() == RED:
                return 0, False

        # Check 4: Validate if black node counts are balanced
        if node.get_left() and node.get_right():
            # check if children are pointed to the parent correctly
            if self.nil != node.get_left() and node != node.get_left().get_parent():
                return 0, False
            if self.nil != node.get_right() and node != node.get_right().get_parent():
                return 0, False

            # Go down each subtree and check if the child nodes are valid
            left_counts, left_ok = self.is_valid_rb_node(node.get_left())
            if not left_ok:
                return 0, False
            right_counts, right_ok = self.is_valid_rb_node(node.get_right())
            if not right_ok:
                return 0, False

            # check if the subtrees are balanced
            if left_counts != right_counts:
                return 0, False
            return left_counts, True
        else:
            return 0, True

    def validate_rb_properties(self):
        black_count, validity = self.is_valid_rb_node(self.root)
        return validity and not self.root.get_color()

    def print_tree(self):
        def visit_node(node):
            if node.get_left():
                visit_node(node.get_left())
                print "[Key: " + str(node.get_key()) + ", color: " + node.get_color() + "] -> Left child: [Key: " + \
                      str(node.get_left().get_key()) + ", color: " + node.get_left().get_color() + "]"
            if node.get_right():
                visit_node(node.get_right())
                print "[Key: " + str(node.get_key()) + ", color: " + node.get_color() + "] -> Right child: [Key: " + \
                      str(node.get_right().get_key()) + ", color: " + node.get_right().get_color() + "]"

        print "Current state of RB tree: Root: [key: " + str(self.root.get_key()) + ", color: " + \
              self.root.get_color() + "]"
        visit_node(self.root)


def generate_tree(t, keys):
    #assert t.validate_rb_properties()
    for i, key in enumerate(keys):
        for k in keys[:i]:
            assert t.nil != t.search(k)
        for k in keys[i:]:
            assert (t.nil == t.search(k)) ^ (k in keys[:i])
        t.insert(key)
    return t


def node_id(node):
    return id(node)


def node_color(node):
    if node.get_color() == RED:
        return "Red"
    else:
        return "Black"


def main():
    # Initialize and print the RB tree
    keys = [10]
    print "Keys used to initialize the RB tree: ", str(keys)
    rbtree = tree()
    rbtree = generate_tree(rbtree, keys)
    rbtree.print_tree()

    # Print the available options to user and wait for the input
    print "Options available:"
    print "1 -> Search"
    print "2 -> Min"
    print "3 -> Max"
    print "4 -> Sort"
    print "5 -> Insert"
    print "6 -> Successor"
    print "7 -> Predecessor"
    print "8 -> Print"
    print "9 -> Exit"
    ip = input('Enter your choice: ')
    while ip in range(1, 9):
        if ip == 1:
            key = input('Enter the key you want to search for: ')
            keyNode = rbtree.search(int(key))
            if keyNode.get_key() is not None:
                print str(node_id(keyNode)) + ": [key: " + str(keyNode.get_key()) + ", color: ", node_color(keyNode) + "]"
            else:
                print "The key was not found in the tree"
        elif ip == 2:
            keyNode = rbtree.min()
            print "Minimum value within the RB tree is: " + str(node_id(keyNode)) + ": [key: " + str(keyNode.get_key()) \
                  + ", color: ", node_color(keyNode) + "]"
        elif ip == 3:
            keyNode = rbtree.max()
            print "Maximum value within the RB tree is: " + str(node_id(keyNode)) + ": [key: " + str(keyNode.get_key()) \
                  + ", color: ", node_color(keyNode) + "]"
        elif ip == 4:
            print "The sorted set of keys is: ", rbtree.sort()
        elif ip == 5:
            newKey = input('Enter the key you want to insert: ')
            rbtree.insert(newKey)
            print "The new key has been inserted into the RB tree"
        elif ip == 6:
            key = input('Enter the key whose successor is to be found: ')
            keyNode = rbtree.successor(key)
            print "[key: " + str(keyNode.get_key()) + ", color: ", node_color(keyNode) + "]"
        elif ip == 7:
            key = input('Enter the key whose predecessor is to be found: ')
            keyNode = rbtree.predecessor(key)
            print "[key: " + str(keyNode.get_key()) + ", color: ", node_color(keyNode) + "]"
        elif ip == 8:
            rbtree.print_tree()
        else:
            break
        ip = input('Enter your choice: ')


if __name__ == "__main__":
    main()