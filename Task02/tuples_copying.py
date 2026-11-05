"""Q2 – Tuples, Mutability and Copying: City Bus-Stop Map."""
import copy
import sys
import time


def main():
    rows, cols = 3, 4

    # Original aliasing bug and corrected grid.
    bad = [[0] * cols] * rows
    bad[0][1] = 7
    good = [[0 for _ in range(cols)] for _ in range(rows)]
    good[0][1] = 7

    print("bad :", bad)
    print("good:", good)
    print(bad[0] is bad[1], good[0] is good[1])

    # Tuple coordinates as dictionary keys.
    stops = {
        (13.0827, 80.2707): "Chennai Central",
        (13.0418, 80.2341): "T. Nagar"
    }
    print(stops[(13.0418, 80.2341)])

    try:
        stops[[13.0418, 80.2341]] = "Invalid list key"
    except TypeError as error:
        print("List key error:", error)

    # Aliasing, shallow copy and deep copy.
    original = [[1, 2], [3, 4]]
    alias = original
    shallow_copy = copy.copy(original)
    slice_copy = original[:]
    deep_copy = copy.deepcopy(original)
    original[0][0] = 99
    print("Aliasing reflects change:", alias)
    print("Shallow copy shares inner list:", shallow_copy)
    print("Slice copy shares inner list:", slice_copy)
    print("Deep copy is independent:", deep_copy)

    # Tuple unpacking.
    for latitude, longitude in stops:
        print("Stop coordinate:", latitude, longitude)

    # A tuple is immutable, but a mutable object inside it can change.
    tuple_with_list = ("zone-A", [1, 2])
    tuple_with_list[1].append(3)
    print("Tuple containing a list after append:", tuple_with_list)

    # Memory comparison: container sizes (not including referenced elements).
    values = list(range(1_000_000))
    tuple_values = tuple(values)
    print("List container size (bytes):", sys.getsizeof(values))
    print("Tuple container size (bytes):", sys.getsizeof(tuple_values))

    # Creation and indexing timing.
    count = 1_000_000
    start = time.perf_counter()
    list_data = list(range(count))
    list_creation = time.perf_counter() - start
    start = time.perf_counter()
    tuple_data = tuple(range(count))
    tuple_creation = time.perf_counter() - start

    start = time.perf_counter()
    _ = list_data[count // 2]
    list_index = time.perf_counter() - start
    start = time.perf_counter()
    _ = tuple_data[count // 2]
    tuple_index = time.perf_counter() - start

    print("List creation time:", round(list_creation, 6), "seconds")
    print("Tuple creation time:", round(tuple_creation, 6), "seconds")
    print("List indexing time:", round(list_index, 9), "seconds")
    print("Tuple indexing time:", round(tuple_index, 9), "seconds")


if __name__ == "__main__":
    main()
