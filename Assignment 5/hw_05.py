import os


# Custom pseudorandom number generator with a random initial seed
class PRNG:
    def __init__(self, seed=None):
        # Use a truly random seed if no seed is provided
        if seed is None:
            seed = int.from_bytes(os.urandom(4), 'big')  # Generate a random 32-bit integer
        self.state = seed

    def randint(self, low, high):
        # Simple linear congruential generator (LCG)
        self.state = (1103515245 * self.state + 12345) % (2 ** 31)
        return low + (self.state % (high - low + 1))


# Generate logistics dataset
def generate_logistics_dataset(num_warehouses=100, max_packages=1000, seed=None):
    """Generates a logistics dataset with a random or specified seed."""
    prng = PRNG(seed)  # Initialize PRNG with the seed or a random one
    data = []
    for i in range(1, num_warehouses + 1):
        warehouse_id = f"WH-{str(i).zfill(3)}"
        priority_level = prng.randint(1, 5)
        package_count = prng.randint(0, max_packages)
        data.append([warehouse_id, priority_level, package_count])
    return data


# Save dataset to a CSV file
def save_to_csv(data, file_name):
    """Saves the dataset to a CSV file."""
    with open(file_name, "w") as file:
        # Write the header
        file.write("Warehouse_ID,Priority_Level,Package_Count\n")
        # Write each row
        for row in data:
            file.write(",".join(map(str, row)) + "\n")


######### YOUR CODE GOES HERE ---  You shoud define here two_level_sorting and the 3 sorting functions

### Your three sorting functions should have global variable named as counter. So do not return it.
def two_level_sorting(function, dataset):
    try:
        # It is checked whether the input is empty or not.
        if len(dataset) < 1:
            raise ValueError

        # It is checked whether there are letters or similar elements in the input that cannot be compared.
        for row in dataset:
            if not isinstance(row[1], (int, str)) or not isinstance(row[2], (int, str)):
                raise TypeError

        sorted_result = dataset.copy()

        # The tasks are sorted according to priority levels and a counter is assigned.
        first_sort = function(sorted_result, 1)
        pl_counter = counter

        # The tasks are sorted according to the number of packages and a counter is assigned.
        final_sort = function(first_sort, 2)
        pc_counter = counter

    except ValueError:
        return dataset, 0, 0
    except TypeError:
        return dataset, 0, 0
    except Exception:
        return dataset, 0, 0

    return final_sort, pl_counter, pc_counter

def bubble_sort(array, index):
    global counter
    counter = 0

    # All PLs are checked in pairs sequentially.
    if index == 1:
        for idx in range(len(array) - 1):
            for i in range(len(array) - 1, idx, -1):
                counter += 1
                if array[i - 1][1] > array[i][1]:
                    array[i - 1], array[i] = array[i], array[i - 1]

    # All PCs are checked in pairs sequentially.
    if index == 2:
        for i in range(1, len(array)):
            for k in range(len(array) - 1, i - 1, -1):
                if array[i - 1][1] == array[k][1] and array[i - 1][2] == array[k][2]:
                    counter += 1
                    if array[i - 1][0] > array[k][0]:
                        array[i - 1], array[k] = array[k], array[i - 1]
                elif array[i - 1][1] == array[k][1]:
                    counter += 1
                    if array[i - 1][2] > array[k][2]:
                        array[i - 1], array[k] = array[k], array[i - 1]

    return array

def merge_sort(array, index):
    global counter
    counter = 0

    def merge(left, right):
        # Here, while the merging process is being done, the elements are checked,
        # and if the value on the right is smaller, the counter is incremented by 1
        global counter
        result = []

        while left and right:
            if index == 1:
                if left[0][1] > right[0][1]:
                    result.append(right.pop(0))
                    counter += 1
                else:
                    result.append(left.pop(0))
            elif index == 2:
                if left[0][2] > right[0][2]:
                    result.append(right.pop(0))
                    counter += 1
                else:
                    result.append(left.pop(0))

        result.extend(left if left else right)
        return result


    def recursive_merge_sort(array):
        # The input is progressively reduced by division.
        if len(array) <= 1:
            return array

        mid = len(array) // 2
        left = recursive_merge_sort(array[:mid])
        right = recursive_merge_sort(array[mid:])

        return merge(left, right)

    if index == 1:
        return recursive_merge_sort(array)

    elif index == 2:
        result = []
        start = 0
        while start < len(array):
            current_priority = array[start][1]
            end = start
            while end < len(array) and array[end][1] == current_priority:
                end += 1

            sorted_group = recursive_merge_sort(array[start:end])
            result.extend(sorted_group)
            start = end

        return result
    return array

def quick_sort(array, index):
    global counter
    counter = 0

    def partition(data, pivot_index, index):
        # The right, left, middle, and pivot are selected.
        pivot = data[pivot_index]
        left = [item for item in data if item[index] < pivot[index]]
        middle = [item for item in data if item[index] == pivot[index]]
        right = [item for item in data if item[index] > pivot[index]]
        return left, middle, right

    def quick_sort_recursive(data, index):
        global counter
        if len(data) <= 1:
            return data

        counter += 1

        pivot_index = len(data) // 2
        left, middle, right = partition(data, pivot_index, index)

        return quick_sort_recursive(left, index) + middle + quick_sort_recursive(right, index)

    if index == 2:
        result = []
        start = 0
        while start < len(array):
            current_pl = array[start][1]
            end = start
            while end < len(array) and array[end][1] == current_pl:
                end += 1

            group = array[start:end]
            result.extend(quick_sort_recursive(group, index))
            start = end

        return result

    return quick_sort_recursive(array, index)


#########

def write_output_file(
        bubble_sorted, merge_sorted, quick_sorted,
        bubble_sort_pl_iterations, merge_sort_pl_counter, quick_sort_pl_counter,
        bubble_sort_pc_iterations, merge_sort_pc_counter, quick_sort_pc_counter,
        merge_check, quick_check
):
    """Write sorted results and comparisons to the output file."""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.write("=== Bubble Sorted Results ===\n")
        # file.write(bubble_sorted.to_string() + "\n\n")
        file.write("Warehouse_ID  Priority_Level  Package_Count\n")
        file.write("-" * 40 + "\n")
        for row in bubble_sorted:
            file.write(f"{row[0]:<12}  {row[1]:<14}  {row[2]:<13}\n")
        file.write("\n")
        file.write("=== Comparison Results ===\n")
        if merge_check:
            file.write("Merge and Bubble sorts are identical.\n")
        else:
            file.write("Merge and Bubble sorts differ.\n")

        if quick_check:
            file.write("Quick and Bubble sorts are identical.\n")
        else:
            file.write("Quick and Bubble sorts differ.\n")

        file.write("\n=== Sort Performance Metrics ===\n")
        file.write(f"Bubble priority sort iteration count: {bubble_sort_pl_iterations}\n")
        file.write(f"Merge priority sort n_of right array is smaller than left: {merge_sort_pl_counter}\n")
        file.write(f"Quick priority sort recursive step count: {quick_sort_pl_counter}\n\n")

        file.write(f"Bubble package count sort iteration count: {bubble_sort_pc_iterations}\n")
        file.write(f"Merge package count n_of right array is smaller than left: {merge_sort_pc_counter}\n")
        file.write(f"Quick package count sort recursive step count: {quick_sort_pc_counter}\n")

    print(f"Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    # File paths and dataset size
    # Specify paths for input and output file
    INPUT_FILE = "C:\\Users\\Umut\\OneDrive\\Masaüstü\\hw05_input.csv"  # Path where the generated dataset will be saved
    OUTPUT_FILE = "C:\\Users\\Umut\OneDrive\\Masaüstü\\hw05_output.txt"  # Path where the sorted results and metrics will be saved
    SIZE = 100  # Number of warehouses in the dataset

    # Generate the dataset
    dataset = generate_logistics_dataset(SIZE,
                                         max_packages=100)  # Generate a dataset with SIZE warehouses and max_packages packages

    # Save the generated dataset to the input file
    save_to_csv(dataset, INPUT_FILE)

    ###############################################################################################################
    # Perform sorting and counting operations
    # Sort using Bubble Sort and count iterations for Priority Level (_pl_) and Package Count (_pc_)
    bubble_sorted, bubble_sort_pl_iterations, bubble_sort_pc_iterations = two_level_sorting(bubble_sort, dataset)

    # Sort using Merge Sort and count recursive steps for Priority Level and Package Count
    merge_sorted, merge_sort_pl_counter, merge_sort_pc_counter = two_level_sorting(merge_sort, dataset)

    # Sort using Quick Sort and count recursive steps for Priority Level and Package Count
    quick_sorted, quick_sort_pl_counter, quick_sort_pc_counter = two_level_sorting(quick_sort, dataset)
    ###############################################################################################################

    # Comparisons
    # Check if Merge Sort results match Bubble Sort results
    merge_check = merge_sorted == bubble_sorted

    # Check if Quick Sort results match Bubble Sort results
    quick_check = quick_sorted == bubble_sorted

    # Write results and metrics to the output file
    write_output_file(
        bubble_sorted, merge_sorted, quick_sorted,
        bubble_sort_pl_iterations, merge_sort_pl_counter, quick_sort_pl_counter,
        bubble_sort_pc_iterations, merge_sort_pc_counter, quick_sort_pc_counter,
        merge_check, quick_check
    )



