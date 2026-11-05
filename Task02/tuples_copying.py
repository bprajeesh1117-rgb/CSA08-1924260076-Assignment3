
"""
TASK 02 – TUPLES, MUTABILITY AND COPYING
Problem Context: City Bus-Stop Map

Requirements:
1. Represent GPS coordinates using tuples as dictionary keys.
2. Create a correct grid using list comprehension.
3. Demonstrate aliasing.
4. Demonstrate shallow copying using copy.copy() and slicing.
5. Demonstrate deep copying using copy.deepcopy().
6. Unpack tuples in a for loop.
7. Demonstrate why tuples can be dictionary keys but lists cannot.
8. Demonstrate the shared-row grid bug using is and id().
9. Compare memory usage of a list and tuple of 1,000,000 values.
10. Compare creation and indexing times.
11. Test a mutable list stored inside a tuple.
12. Demonstrate function argument mutation.
13. Demonstrate a sparse dictionary grid alternative.
"""

import copy
import sys
import time


def grid_demonstration():
    print("\n" + "=" * 60)
    print("GRID CREATION AND ALIASING")
    print("=" * 60)

    rows, cols = 3, 4

    bad = [[0] * cols] * rows
    bad[0][1] = 7

    good = [[0 for _ in range(cols)] for _ in range(rows)]
    good[0][1] = 7

    print("Bad grid:", bad)
    print("Good grid:", good)

    print("\nIDENTITY TEST")
    print("Bad rows are identical:", bad[0] is bad[1])
    print("Good rows are identical:", good[0] is good[1])

    print("Bad row IDs:", [id(row) for row in bad])
    print("Good row IDs:", [id(row) for row in good])


def tuple_dictionary():
    print("\n" + "=" * 60)
    print("TUPLES AS DICTIONARY KEYS")
    print("=" * 60)

    stops = {
        (13.0827, 80.2707): "Chennai Central",
        (13.0418, 80.2341): "T. Nagar",
        (13.0674, 80.2376): "Kodambakkam"
    }

    print("Bus stop dictionary:", stops)
    print("Chennai Central:", stops[(13.0827, 80.2707)])
    print("T. Nagar:", stops[(13.0418, 80.2341)])

    print("\nTUPLE UNPACKING")

    for (latitude, longitude), stop_name in stops.items():
        print(
            f"{stop_name}: Latitude = {latitude}, "
            f"Longitude = {longitude}"
        )

    print("\nLIST AS DICTIONARY KEY")

    try:
        invalid_key = [13.0418, 80.2341]
        sample = {invalid_key: "T. Nagar"}
    except TypeError as error:
        print("Error:", error)

    print("Tuples can be dictionary keys because they are immutable.")
    print("Lists cannot be dictionary keys because they are mutable.")


def copying_demonstration():
    print("\n" + "=" * 60)
    print("ALIASING AND COPYING")
    print("=" * 60)

    original = [10, 20, 30]
    alias = original

    shallow_copy = copy.copy(original)
    slicing_copy = original[:]

    print("Original:", original)
    print("Alias:", alias)
    print("Shallow copy:", shallow_copy)
    print("Slicing copy:", slicing_copy)

    print("\nIDENTITY COMPARISON")
    print("Original is alias:", original is alias)
    print("Original is shallow copy:", original is shallow_copy)
    print("Original is slicing copy:", original is slicing_copy)

    alias.append(40)

    print("\nAFTER MODIFYING ALIAS")
    print("Original:", original)
    print("Alias:", alias)
    print("Shallow copy:", shallow_copy)

    print("\nNESTED LIST COPYING")

    nested_original = [[1, 2], [3, 4]]

    shallow = copy.copy(nested_original)
    slicing = nested_original[:]
    deep = copy.deepcopy(nested_original)

    nested_original[0][0] = 99

    print("Original:", nested_original)
    print("Shallow copy:", shallow)
    print("Slicing copy:", slicing)
    print("Deep copy:", deep)

    print("\nSHALLOW COPY IDENTITY")
    print("Outer objects identical:", nested_original is shallow)
    print("Inner objects identical:", nested_original[0] is shallow[0])

    print("\nDEEP COPY IDENTITY")
    print("Outer objects identical:", nested_original is deep)
    print("Inner objects identical:", nested_original[0] is deep[0])


def modify_list(values):
    values.append(100)
    values[0] = 999


def function_mutability():
    print("\n" + "=" * 60)
    print("FUNCTION ARGUMENT MUTABILITY")
    print("=" * 60)

    numbers = [10, 20, 30]

    print("Before function call:", numbers)
    modify_list(numbers)
    print("After function call:", numbers)


def mutable_inside_tuple():
    print("\n" + "=" * 60)
    print("LIST INSIDE A TUPLE")
    print("=" * 60)

    data = ("Chennai", [10, 20, 30])

    print("Original tuple:", data)

    data[1].append(40)

    print("After modifying the inner list:", data)
    print("The tuple cannot be reassigned, but its inner list is mutable.")


def memory_comparison():
    print("\n" + "=" * 60)
    print("MEMORY COMPARISON: 1,000,000 VALUES")
    print("=" * 60)

    n = 1_000_000

    list_data = list(range(n))
    tuple_data = tuple(range(n))

    list_memory = sys.getsizeof(list_data)
    tuple_memory = sys.getsizeof(tuple_data)

    print("Number of values:", n)
    print("List container memory:", list_memory, "bytes")
    print("Tuple container memory:", tuple_memory, "bytes")

    print("List container memory:", round(list_memory / (1024 * 1024), 2), "MB")
    print("Tuple container memory:", round(tuple_memory / (1024 * 1024), 2), "MB")

    print("Note: sys.getsizeof() measures the container itself,")
    print("not all referenced objects.")


def creation_time_comparison():
    print("\n" + "=" * 60)
    print("LIST AND TUPLE CREATION TIME")
    print("=" * 60)

    n = 1_000_000
    repetitions = 5

    start = time.perf_counter()

    for _ in range(repetitions):
        list_data = list(range(n))

    list_time = (time.perf_counter() - start) / repetitions

    start = time.perf_counter()

    for _ in range(repetitions):
        tuple_data = tuple(range(n))

    tuple_time = (time.perf_counter() - start) / repetitions

    print("Number of values:", n)
    print(f"Average list creation time: {list_time:.6f} seconds")
    print(f"Average tuple creation time: {tuple_time:.6f} seconds")


def indexing_time_comparison():
    print("\n" + "=" * 60)
    print("LIST AND TUPLE INDEXING TIME")
    print("=" * 60)

    n = 1_000_000

    list_data = list(range(n))
    tuple_data = tuple(list_data)

    indices = [i % n for i in range(100_000)]

    start = time.perf_counter()

    for index in indices:
        value = list_data[index]

    list_time = time.perf_counter() - start

    start = time.perf_counter()

    for index in indices:
        value = tuple_data[index]

    tuple_time = time.perf_counter() - start

    print("Number of indexing operations:", len(indices))
    print(f"List indexing time: {list_time:.6f} seconds")
    print(f"Tuple indexing time: {tuple_time:.6f} seconds")


def sparse_grid_demonstration():
    print("\n" + "=" * 60)
    print("SPARSE DICTIONARY GRID ALTERNATIVE")
    print("=" * 60)

    rows, cols = 3, 4

    passenger_zones = {
        (0, 1): 7,
        (1, 2): 5,
        (2, 3): 10
    }

    print("Sparse grid:", passenger_zones)
    print("Passengers in zone (0, 1):",
          passenger_zones.get((0, 1), 0))
    print("Passengers in zone (0, 0):",
          passenger_zones.get((0, 0), 0))

    print("\nFULL GRID REPRESENTATION")

    for row in range(rows):
        row_values = []

        for col in range(cols):
            row_values.append(passenger_zones.get((row, col), 0))

        print(row_values)

    print("\nCOMPLEXITY COMPARISON")
    print("List of lists access time: O(1)")
    print("List of lists space: O(rows * columns)")
    print("Sparse dictionary average access time: O(1)")
    print("Sparse dictionary space: O(number of non-empty zones)")


def main():
    print("=" * 60)
    print("TASK 02 – TUPLES, MUTABILITY AND COPYING")
    print("=" * 60)

    # Complete Code: TODO 1

    rows, cols = 3, 4

    bad = [[0] * cols] * rows
    bad[0][1] = 7

    # Create a rows x cols grid with separate row objects.
    good = [[0 for _ in range(cols)] for _ in range(rows)]

    good[0][1] = 7

    print("\nCOMPLETE THE CODE – EXPECTED OUTPUT")
    print("bad :", bad)
    print("good:", good)
    print(bad[0] is bad[1], good[0] is good[1])

    # Tuple dictionary keys

    stops = {
        (13.0827, 80.2707): "Chennai Central",
        (13.0418, 80.2341): "T. Nagar"
    }

    print(stops[(13.0418, 80.2341)])

    # Other demonstrations

    grid_demonstration()
    tuple_dictionary()
    copying_demonstration()
    function_mutability()
    mutable_inside_tuple()
    memory_comparison()
    creation_time_comparison()
    indexing_time_comparison()
    sparse_grid_demonstration()

    print("\n" + "=" * 60)
    print("TASK 02 COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
