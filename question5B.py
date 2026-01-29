"""The problem is about sorting a list of numbers using multithreading. Instead of sorting the entire
list using a single process, the idea is to divide the work among multiple threads so that different 
parts of the list are processed at the same time. This helps us understand how parallel execution works
in programming. The task is to split the array into parts, sort those parts independently using separate 
threads, and then combine (merge) the sorted parts to produce the final sorted list. 
The focus of the problem is not just sorting, but also demonstrating the correct use of threads, 
synchronization, and merging of results."""

"""To solve this problem, we first divide the original list into two equal halves. 
Then, we create two separate threads, where one thread sorts the left half of the list and the other 
thread sorts the right half. These two threads run independently and simultaneously. 
Once both sorting threads finish their work, we wait for them using the join() method to make sure sorting 
is complete. After that, we create a third thread whose job is to merge the two sorted halves into a
single sorted list using a standard merge technique (similar to merge sort). Finally, 
the merged list is returned as the fully sorted result. This approach clearly demonstrates 
how multiple threads can cooperate to solve a single problem while maintaining correct execution order."""

import threading

def multithreaded_sort(arr):
    """
    This function sorts a list using 3 threads:
    - Thread 1 sorts the left half
    - Thread 2 sorts the right half
    - Thread 3 merges both sorted halves into the final sorted list
    """

    # If the list has 0 or 1 element, it is already sorted
    if len(arr) <= 1:
        return arr

    # Step 1: Split the list into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # We store results in lists so threads can update them
    # (because threads cannot directly return values)
    sorted_left = [None]
    sorted_right = [None]

    # Step 2: Thread function to sort the left half
    def sort_left():
        sorted_left[0] = sorted(left_half)  # sort left half
        print("Thread 1 sorted left :", sorted_left[0])

    # Step 3: Thread function to sort the right half
    def sort_right():
        sorted_right[0] = sorted(right_half)  # sort right half
        print("Thread 2 sorted right:", sorted_right[0])

    # Create two threads for sorting
    t1 = threading.Thread(target=sort_left)
    t2 = threading.Thread(target=sort_right)

    # Start both sorting threads
    t1.start()
    t2.start()

    # Wait until both sorting threads finish
    t1.join()
    t2.join()

    # Step 4: Merge function (combines two sorted lists into one sorted list)
    def merge_two_sorted_lists(a, b):
        result = []
        i = 0  # pointer for list a
        j = 0  # pointer for list b

        # Compare elements and pick the smaller one each time
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:               # <= helps handle duplicates nicely
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1

        # Add remaining elements (only one of these will have items left)
        result.extend(a[i:])
        result.extend(b[j:])

        return result

    # We store final result here so merge thread can update it
    final_result = [None]

    # Step 5: Thread function to merge the two sorted halves
    def merge_thread():
        final_result[0] = merge_two_sorted_lists(sorted_left[0], sorted_right[0])
        print("Thread 3 merged both halves successfully.")

    # Create and run merge thread
    t3 = threading.Thread(target=merge_thread)
    t3.start()
    t3.join()

    # Return the final sorted list
    return final_result[0]


# -------------------- User Test --------------------
if __name__ == "__main__":
    original_list = [7, 12, 19, 3, 18, 4, 2, 6, 15, 8]
    print("Original list:", original_list)

    sorted_list = multithreaded_sort(original_list)
    print("Sorted list  :", sorted_list)