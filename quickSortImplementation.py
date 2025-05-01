import random
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
sys.setrecursionlimit(50000)

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def qs_last(arr):
    stack = [arr]
    result = []
    while stack:
        current = stack.pop()
        if len(current) <= 25:
            result.extend(insertion_sort(current))
        elif len(current) > 1:
            pivot = current.pop()
            items_lower = [item for item in current if item <= pivot]
            items_greater = [item for item in current if item > pivot]
            stack.append(items_greater)
            result.append(pivot)
            stack.append(items_lower)
        else:
            result.extend(current)
    return result

def qs_first(arr):
    stack = [arr]
    result = []
    while stack:
        current = stack.pop()
        if len(current) <= 25:
            result.extend(insertion_sort(current))
        elif len(current) > 1:
            pivot = current.pop(0)
            items_lower = [item for item in current if item <= pivot]
            items_greater = [item for item in current if item > pivot]
            stack.append(items_greater)
            result.append(pivot)
            stack.append(items_lower)
        else:
            result.extend(current)
    return result

def qs_random(arr):
    stack = [arr]
    result = []
    while stack:
        current = stack.pop()
        if len(current) <= 25:
            result.extend(insertion_sort(current))
        elif len(current) > 1:
            pivot_index = np.random.randint(0, len(current))
            pivot = current.pop(pivot_index)
            items_lower = [item for item in current if item <= pivot]
            items_greater = [item for item in current if item > pivot]
            stack.append(items_greater)
            result.append(pivot)
            stack.append(items_lower)
        else:
            result.extend(current)
    return result

def qs_median(arr):
    stack = [arr]
    result = []
    while stack:
        current = stack.pop()
        if len(current) <= 25:
            result.extend(insertion_sort(current))
        elif len(current) > 1:
            if len(current) >= 3:
                first = current[0]
                middle = current[len(current) // 2]
                last = current[-1]
                if first <= middle <= last or last <= middle <= first:
                    pivot_index = len(current) // 2
                elif middle <= first <= last or last <= first <= middle:
                    pivot_index = 0
                else:
                    pivot_index = len(current) - 1
            else:
                pivot_index = 0
            pivot = current.pop(pivot_index)
            items_lower = [item for item in current if item <= pivot]
            items_greater = [item for item in current if item > pivot]
            stack.append(items_greater)
            result.append(pivot)
            stack.append(items_lower)
        else:
            result.extend(current)
    return result

def measure_time(sort_func, arr):
    start_time = time.time()
    sort_func(arr.copy())
    return time.time() - start_time

def measure_average_time(sort_func, arr, runs=15):
    total_time = 0
    for _ in range(runs):
        total_time += measure_time(sort_func, arr)
    return total_time / runs

data = [100, 1000]
array_types = ["Random", "Ascending", "Descending", "Duplicates"]
results = {size: {atype: [] for atype in array_types} for size in data}

for size in data:
    arr = np.random.randint(0, 100000, size).tolist()
    arr_asc = sorted(arr)
    arr_desc = sorted(arr, reverse=True)
    arr_dup = [random.choice(arr) for _ in range(size)]
    
    print(f"Array size: {size}")
    
    for atype, test_array in zip(array_types, [arr, arr_asc, arr_desc, arr_dup]):
        avg_times = []
        for sort_func in [qs_last, qs_first, qs_random, qs_median]:
            avg_time = measure_average_time(sort_func, test_array)
            avg_times.append(avg_time)
            print(f"{sort_func.__name__} ({atype}): {avg_time:.6f} seconds")
        results[size][atype] = avg_times
    print("\n")

for size in data:
    plt.figure(figsize=(10, 6))
    for atype in array_types:
        plt.plot(["Last", "First", "Random", "Median"], results[size][atype], label=f"{atype} Array")
    plt.title(f"Average Sorting Time for Array Size {size} (15 Runs)")
    plt.xlabel("Pivot Selection Method")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid()
    plt.show()