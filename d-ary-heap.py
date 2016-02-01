

# Function signature: maxHeapify(Array, Integer, Integer, Integer)
# This function accepts an array and recursively calls itself such that the logical heap
# is a max-heap around initial element at index i within the array.
# Arguments:
#  array - the array to be max-heapified
#  i - the index of the element around which we need to max-heapify
#  d - maximum number of children possible for each node
#  heapSize - the position upto which the logical tree has been max-heapified
# Returns: A max-heap around the initial index i
def maxHeapify(array, i, d, heapSize):
    # Get hold of the index of left-most and right-most children of the node at i
    # For 1 based index:
    # minChildIndex = (d * (i - 1)) + 2
    # maxChildIndex = (d * i) + 1
    # For 0 based index:
    minChildIndex = (d * i) + 1
    maxChildIndex = (i + 1) * d

    arrayLen = len(array)

    # The number of children could be 0. If so, return the array without processing
    # any further.
    if minChildIndex > (arrayLen - 1):
        return array

    largestValIndex = i

    # The number of elements in the bottom-most level could be less than d. Perform
    # explicit check to make sure if this is the case.
    if (arrayLen - 1) < maxChildIndex:
        maxChildIndex = arrayLen

    # Now iterate through each child and check if all children are less than the value
    # stored at i. If not find the largest child and swap the values at that position
    # and that stored at i.
    # Note: Since the function calls are recursive in nature, the tree gets
    # max-heapified from the bottom and we track this through a variable heapSize.
    for currChildIndex in range(minChildIndex, maxChildIndex + 1):
        if (currChildIndex <= heapSize) \
                and (array[largestValIndex] < array[currChildIndex]):
            largestValIndex = currChildIndex

    # If the value stored at i is less than any of the child values, exchange it with
    # the largest child value and call max-heapify on this child index
    if largestValIndex != i:
        # Swapping the values
        temp = array[largestValIndex]
        array[largestValIndex] = array[i]
        array[i] = temp
        # Recursive call on this child index
        array = maxHeapify(array, largestValIndex, d, heapSize)

    # Return the processed array
    return array


# Function signature: buildMaxHeap(Array, Integer)
# This function goes through each element in the tree and makes it a max-heap
# Arguments:
#  array - the array to be processed
#  d - maximum number of children a node can have
# Result: The complete array in the form of a max heap and the heap-size
def buildMaxHeap(array, d):
    # local variables
    heapSize = len(array) - 1

    # At the initial call, all the elements from array[n//d ... n] will be the nodes
    # from the bottom-most level of the d-ary heap. These nodes will have a single
    # element in them and no children. We start processing nodes and go up the
    # tree so that for each node, the children will already be max-heapified.
    for currIndex in range((len(array) // d) - 1, -1, -1):
        array = maxHeapify(array, currIndex, d, heapSize)

    return array, heapSize


# Function signature: heapSort(Array, Integer)
# This function performs sorting on the array passed in as argument by constantly
# building max-heaps around the first element in the array and then moving this
# largest value to a position designated by the variable heapSize
# Arguments:
#  array - the array to be sorted
#  d - maximum number of children possible for a node
# Result: the sorted array
def heapSort(array, d):
    # Build a max heap out of the array which is passed in
    res, heapSize = buildMaxHeap(array, d)

    # Now the first element of the array has the highest value in the given list.
    # We need to move this value to the end of the list and mark is using a flag
    # such that it is no longer processed. This is taken care of by the heapSize
    # variable which is initialized within the buildMaxHeap() method.
    for currIndex in range(len(array) - 1, 0, -1):
        # Swapping the values
        temp = array[currIndex]
        array[currIndex] = array[0]
        array[0] = temp

        # Reduce the heap size so that the next iteration doesn't process the
        # swapped element
        heapSize -= 1

        # Call max-heapify on the first element in the array
        res = maxHeapify(array, 0, d, heapSize)

    return res


# Function Signature: heapExtractMax(Array, Integer, Integer)
# This function extracts the maximum value stored in the array and returns it to
# the caller. After this step, the function decrements the heap-size and runs
# max-heapify on the remaining elements.
# Arguments:
#  array - the array from which the max value has to be extracted
#  d - maximum number of children possible for any node
#  heapSize - the index in the array upto which elements need to be processed
# Returns: maximum value in the array, array after extracting this element, and
#          the updated value for heap-size
def heapExtractMax(array, d, heapSize):
    if heapSize < 0:
        raise Exception("Array underflow error")

    # Read the maximum value in the array which is always the first element and
    # replace it with a copy of the last unprocessed element
    maxVal = array[0]
    array[0] = array[heapSize]

    # Used to keep track how many elements have been removed from the array
    heapSize -= 1

    # The updated array which will contain duplicate elements since the first
    # element was replced with a copy of the last unprocessed element
    res = maxHeapify(array, 0, d, heapSize)

    return maxVal, res, heapSize


# Function signature: findParentIndex(Integer, Integer)
# This function finds the parent of a given index i and returns it
# Arguments:
#  i - the index whose parent is to be found
#  d - maximum number of children possible for any node
# Returns: an integer which specified the parent of i
def findParentIndex(i, d):
    floatDiv = float(i) / float(d)
    floorDiv = float(i // d)
    if floatDiv == floorDiv:
        return int(floorDiv - 1)
    else:
        return int(floorDiv)


# Function signature: heapIncreaseKey(Array, Integer, Integer, Integer)
# This function replaces the value at position i with the value specified by
# the argument named key and then does a process similar to insertion sort
# such that new value is moved to the correct position within an array
# Arguments:
#  array - the array being processed
#  d - maximum number of children possible for any node
#  i - the index at which the new value is to be placed
#  key - the new value to be replaced
# Returns: an updated array which contains the key at its correct position
def heapIncreaseKey(array, d, i, key):
    if key < array[i]:
        raise Exception("The new key is less than the current key")

    array[i] = key
    parentOfI = findParentIndex(i, d)

    # We need to move the key up to its actual position if the parent's value
    # is less than key
    while i > 0 and array[i] > array[parentOfI]:
        # Swap the key with its parent's value
        temp = array[i]
        array[i] = array[parentOfI]
        array[parentOfI] = temp

        # Move the pointer to the parent and continue processing so that the
        # value is moved on to the correct position
        i = parentOfI
        parentOfI = findParentIndex(i, d)

    return array


# Function signature: maxHeapInsert(Array, Integer, Integer, Integer)
# This function adds a new key to a given max-heap and extends it such that it
# meets the max-heap property.
# Arguments:
#  array - the max-heap to be extended
#  d - maximum number of children any node can have
#  key - the new value to be added into the max-heap
#  heapSize - the index upto which the array is unprocessed
# Returns: the max-heap updated with the new key
def maxHeapInsert(array, d, key, heapSize):
    # Extend the array and append a container at its end
    heapSize += 1
    array.append(-1)
    # Add the key and move it to its correct position
    return heapIncreaseKey(array, d, heapSize, key)


# Main function which calls all the functions
def main():
    array1 = [5, 3, 17, 10, 84, 19, 6, 22, 9]
    d1 = 2
    print "Input array: ", array1, ", d = ", d1

    res1, heapSize1 = buildMaxHeap(array1, d1)
    print "Max-heapified array 1:", res1, ", heap size: ", heapSize1

    maxVal, res2, heapSize2 = heapExtractMax(res1, d1, heapSize1)
    print "Max value: ", maxVal, ", Curr Array: ", res2, ", heap size: ", heapSize2
    maxVal, res3, heapSize3 = heapExtractMax(res2, d1, heapSize2)
    print "Max value: ", maxVal, ", Curr Array: ", res3, ", heap size: ", heapSize3

    array2 = [5, 3, 17, 10, 84, 19, 6, 22, 9]
    d2 = 2
    print "Input array: ", array2, ", d = ", d2

    res4 = heapSort(array2, d2)
    print "Sorted array 2: ", res4

    array3 = [5, 3, 17, 10, 84, 19, 6, 22, 9]
    d3 = 2
    print "Input array: ", array3, ", d = ", d3
    res5, heapSize5 = buildMaxHeap(array3, d3)
    print "Max-heapified array 1:", res5, ", heap size: ", heapSize5
    res6 = heapIncreaseKey(res5, d3, 3, 25)
    print "Updated max-heap: ", res6

    print "Input array: ", res5, ", d = ", d3, ", heap size: ", heapSize5
    res7 = maxHeapInsert(res5, d3, 100, heapSize5)
    print "Extended max-heap: ", res7


if __name__ == "__main__":
    main()