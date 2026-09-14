import math

def shellSort(array):
    n = len(array)
    array = [int(i) for i in array if i.isdigit()]
    if len(array) != (n):
        return ["err"]  
    k = int(math.log2(n))
    interval = 2**k -1
    while interval > 0:
        for i in range(interval, n):
            temp = array[i]
            j = i
            while j >= interval and array[j - interval] > temp:
                array[j] = array[j - interval]
                j -= interval
            array[j] = temp
        k -= 1
        interval = 2**k -1
    return array