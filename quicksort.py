# Quick Sort

# Function signature: quicksort(Array, Integer, Integer)
# The main function which starts the quick sort process. This functions splits the array into subarrays and calls
# quicksort on these two arrays. This is the divide part of divide and conquer strategy applied to sort the whole
# array.
# Initial call is: quicksort(array, 1, len(array))
# Arguments:
#  array -> Array to be sorted
#  p -> start index as an Integer
#  r -> end index as an Integer
# Returns: the sorted array
def quicksort(array, p, r):
    if p < r:
        array, q = partition(array, p, r)
        quicksort(array, p, q - 1)
        quicksort(array, q + 1, r)
    return array


# Function signature: partition(Array, Integer, Integer)
# This function sorts the array around the value stored at index r of the array. Towards the end, we have three
# sub-arrays such that A[1...q-1] < A[q] < A[q+1, r].
def partition(array, p, r):
    val = array[r]
    i = p - 1
    for j in [p, r - 1]:
        if array[j] <= val:
            i += 1
            # Swap the values stored in j and i
            # This step is done to make sure that all the values till index i are less than the value stored at
            # index r and the values towards the right of index i are greater than that stored at r
            temp = array[j]
            array[j] = array[i]
            array[i] = temp
    # Swap the value stored at r with the value stored at i + 1 so that it is moved to the right position
    temp = array[i + 1]
    array[i + 1] = array[r]
    array[r] = temp
    return array, i + 1