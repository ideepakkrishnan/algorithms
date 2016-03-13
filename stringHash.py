# ---------------------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------------------

hashTable = []

# ---------------------------------------------------------------
# CLASSES
# ---------------------------------------------------------------


# This class stores the structure of each node within the linked list. Each node has the following properties:
# val - the value stored at the node
# nxt - the node that follows the current node in the linked list
class node:

    def get_key(self):
        return self.key

    def set_key(self, newKey):
        self.key = newKey

    def get_val(self):
        return self.val

    def increment_val(self, step):
        self.val += step

    def get_nxt(self):
        return self.nxt

    def set_nxt(self, newNxt):
        self.nxt = newNxt

    def get_prev(self):
        return self.prev

    def set_prev(self, newPrev):
        self.prev = newPrev

    def get_pos(self):
        return self.posList

    def add_pos(self, newPos):
        self.posList.append(newPos)

    def __init__(self, key, val, nxt, prev, posList):
        self.key = key
        self.val = val
        self.nxt = nxt
        self.prev = prev
        self.posList = posList

# ---------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------


def findPow(length):
    p = 0
    while length >= 2:
        p += 1
        length /= 2
    if length > 1:
        p += 1
    return p


def getTableLength(length):
    power = findPow(length)
    primes = [53,53,53,53,53,53,97,193,389,769,1543,3079,6151,12289,24593,49157,98317,196613,393241,786433,1572869,
              3145739,6291469,12582917,25165843,50331653,100663319,201326611,402653189,805306457,1610612741]
    if power > 31:
        return primes[30]
    return primes[power - 1]


def generateHashVal(word):
    hashVal = 0
    word = word.strip('.').strip('!').strip('(').strip(')').strip('?').lower()
    for i in range(0, len(word)):
        hashVal = 33*hashVal + ord(word[i])
    return hashVal


# ---------------------------------------------------------------
# Hash table operations
# ---------------------------------------------------------------

def increase(key, pos, hashKey):
    res = find(key, hashKey)
    if res is not None:
        res.increment_val(1)
        res.add_pos(pos)
        return True
    return False


def find(word, hashKey):
    global hashTable

    currNode = hashTable[hashKey]
    while currNode.get_val() != -1:
        if currNode.get_key() == word.lower():
            return currNode
        currNode = currNode.get_nxt()
    return None


def insert(word, pos):
    global hashTable

    # Generate the hash value for this word
    hashVal = generateHashVal(word)

    # Find the bucket where the word has to be inserted
    hashKey = hashVal % len(hashTable)

    # Search for the word at the list associated with the key within the hash table. If we find the word, increment
    # the count and add the position to the node object. Else create a new node and add it to the head of the list

    if increase(word, pos, hashKey):
        # The word already exists in the text. The count and position has been updated to the list.
        return True
    else:
        # Insert the word at the head of the list associated with the bucket after initializing a node object
        newWord = node(word, 1, None, None, [pos])
        # Updating the pointers for current head and new word. The new node is added to the head of the list
        hashTable[hashKey].set_prev(newWord)
        newWord.set_nxt(hashTable[hashKey])
        hashTable[hashKey] = newWord
        return True
    return False


def delete(key):
    global hashTable

    hashVal = generateHashVal(key)
    hashKey = hashVal % len(hashTable)
    wordNode = find(key, hashKey)
    if wordNode is not None:
        print "Removing '" + wordNode.get_key() + "' from positions: " + str(wordNode.get_pos())
        # Update the pointers for prev and next node
        if wordNode.get_prev() is not None:
            wordNode.get_prev().set_nxt(wordNode.get_nxt())
        wordNode.get_nxt().set_prev(wordNode.get_prev())
        return True
    else:
        return False


def listAllKeys():
    global hashTable
    keys = []
    for i in range(0, len(hashTable)):
        currNode = hashTable[i]
        while currNode.get_val() != -1:
            keys.append("key: "+currNode.get_key()+", value: "+str(currNode.get_val())+", positions: "+str(currNode.get_pos()))
            currNode = currNode.get_nxt()
        print "Current bucket: ", i, ", Entries: ", keys
        keys = []


# ---------------------------------------------------------------
# Main Function
# ---------------------------------------------------------------

def main():
    global hashTable

    # Process the input file and find the hash table size
    text_file = open("ip.txt", "r")
    text_lines = text_file.readlines()
    text_file.close()
    text = ' '.join(text_lines).split()
    tableLength = getTableLength(len(text))

    # Initialize the hash table
    # Each index is initialized with an empty node which stays at the end of the list as it expands
    hashTable = [node(None, -1, None, None, -1) for i in range(0, tableLength)]

    # Insert each word from the input text into hash table
    for i in range(1, len(text) + 1):
        insert(text[i - 1], i)

    # Listing all the keys in the table
    print "# ---------------------------------------------------------------"
    print "# After initialization"
    print "# ---------------------------------------------------------------"
    listAllKeys()

    # Deleting a key
    keyToBeRemoved = "But"
    print "# ---------------------------------------------------------------"
    print "# Deleting '" + keyToBeRemoved + "' from the hash table"
    print "# ---------------------------------------------------------------"
    if delete(keyToBeRemoved):
        print "All instances of '" + keyToBeRemoved + "' were removed successfully!"
        # Listing all the keys in the table again
        listAllKeys()
    else:
        print "No instances found for '" + keyToBeRemoved + "'!"


if __name__ == "__main__":
    main()