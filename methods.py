import asyncio
import time
from scraper import flipkart
import json

# Async sorting functions (no change to sorting algorithms themselves)
def final_dict(final_dict_all_info, all_info, text, arr):
    final_dict_all_info[text] = {}
    for i in arr:
        final_dict_all_info[text][i] = all_info[i]
    return final_dict_all_info

def final_dict(final_dict_all_info, all_info, text, arr):
    final_dict_all_info[text] = {}
    for i in arr:
        final_dict_all_info[text][i] = all_info[i]
    return final_dict_all_info

def multi_way_merge_sort(final_dict_all_info, all_info, text, arr, k=3):
    """Multi-way merge sort implementation."""
    if len(arr) <= 1:
        return arr

    n = len(arr)
    sublist_size = n // k
    sublists = []

    for i in range(k):
        start = i * sublist_size
        end = (i + 1) * sublist_size if i < k - 1 else n
        sublists.append(sorted(arr[start:end]))

    result = []
    while any(sublists):
        min_val = float('inf')
        min_index = -1

        for i, sublist in enumerate(sublists):
            if sublist and sublist[0] < min_val:
                min_val = sublist[0]
                min_index = i

        result.append(min_val)
        sublists[min_index] = sublists[min_index][1:]

    return final_dict(final_dict_all_info, all_info, text, result)

def heapify(arr, n, i):
    """Heapify a subtree rooted at index i."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(final_dict_all_info, all_info, text, arr):
    """Heap sort implementation."""
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return final_dict(final_dict_all_info, all_info, text, arr)

def shell_sort(final_dict_all_info, all_info, text, arr):
    """Shell sort implementation."""
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return final_dict(final_dict_all_info, all_info, text, arr)


async def algorithms(name_of_product):
    name_of_product = "pen"
    final_dict_all_info = {}

    start_time = time.time()
    text = "Original Data or Web Scrapped Data"
    all_info, prices_list = await flipkart(name_of_product)
    final_dict(final_dict_all_info, all_info, text, prices_list)
    final_dict_all_info[text]["Time Taken For Web Scrapping in seconds"] = time.time() - start_time

    # Multi-way Merge Sort (Synchronous as it doesn't involve I/O operations)
    data_copy = prices_list[:]
    start_time = time.time()
    text = "Data Sorted Using Multi-way Merge Sort"
    multi_way_merge_sort(final_dict_all_info, all_info, text, data_copy)
    final_dict_all_info[text]["Time Taken For Multi-way Merge Sort in seconds"] = time.time() - start_time

    # Heap Sort
    data_copy = prices_list[:]
    start_time = time.time()
    text = "Data Sorted Using Heap Sort"
    heap_sort(final_dict_all_info, all_info, text, data_copy)
    final_dict_all_info[text]["Time Taken For Heap Sort in seconds"] = time.time() - start_time

    # Shell Sort
    data_copy = prices_list[:]
    start_time = time.time()
    text = "Data Sorted Using Shell Sort"
    shell_sort(final_dict_all_info, all_info, text, data_copy)
    final_dict_all_info[text]["Time Taken For Shell Sort in seconds"] = time.time() - start_time

    print(json.dumps(final_dict_all_info, indent=4))
