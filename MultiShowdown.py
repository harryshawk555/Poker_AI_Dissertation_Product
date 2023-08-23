import statistics
import itertools

def indexer(list, filter):
    count = 0 
    for x in list:
        if x[0] == filter:
            return count
        else:
            count += 1

