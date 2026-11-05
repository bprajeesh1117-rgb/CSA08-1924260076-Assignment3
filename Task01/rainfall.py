"""
Q1 – LISTS AND SLICING: DAILY RAINFALL RECORDS

PSEUDOCODE:
1. Generate 365 random rainfall readings.
2. Divide readings into weekly groups using slicing.
3. Calculate weekly rainfall totals.
4. Find the wettest and driest weeks.
5. Find maximum and minimum daily rainfall and their positions.
6. Calculate 7-day moving averages using naive and running-sum methods.
7. Identify dry days.
8. Demonstrate list slicing and list operations.
9. Compare operation counts and execution times.
10. Test empty and shorter-than-seven lists.
11. Demonstrate deque and dictionary alternatives.
"""

import random
import time
from collections import deque
from datetime import date, timedelta


# 1. NAIVE MOVING AVERAGE

def naive_moving_average(values, window=7):
    if window <= 0:
        raise ValueError("Window size must be positive")

    if len(values) < window:
        return []

    averages = []

    for i in range(len(values) - window + 1):
        averages.append(sum(values[i:i + window]) / window)

    return averages


# 2. RUNNING-SUM MOVING AVERAGE

def running_moving_average(values, window=7):
    if window <= 0:
        raise ValueError("Window size must be positive")

    if len(values) < window:
        return []

    averages = []
    total = sum(values[:window])
    averages.append(total / window)

    for i in range(window, len(values)):
        total -= values[i - window]
        total += values[i]
        averages.append(total / window)

    return averages


# 3. DEQUE MOVING AVERAGE

def deque_moving_average(values, window=7):
    if window <= 0:
        raise ValueError("Window size must be positive")

    window_data = deque(maxlen=window)
    averages = []

    for value in values:
        window_data.append(value)

        if len(window_data) == window:
            averages.append(sum(window_data) / window)

    return averages


# 4. DICTIONARY-BASED MOVING AVERAGE

def dictionary_moving_average(values):
    start_date = date(2025, 1, 1)

    rainfall_by_date = {
        start_date + timedelta(days=i): value
        for i, value in enumerate(values)
    }

    averages = []
    current_date = start_date

    for i in range(len(values) - 6):
        total = 0

        for j in range(7):
            day = current_date + timedelta(days=i + j)
            total += rainfall_by_date[day]

        averages.append(total / 7)

    return rainfall_by_date, averages


# 5. OPERATION COUNT COMPARISON

def compare_operation_counts(n, window=7):
    if n < window:
        print("Not enough readings.")
        return

    naive_additions = (n - window + 1) * (window - 1)
    running_additions = n - 1
    running_subtractions = n - window

    print("Number of readings:", n)
    print("Naive additions:", naive_additions)
    print("Running-sum additions:", running_additions)
    print("Running-sum subtractions:", running_subtractions)


# 6. PERFORMANCE BENCHMARK

def benchmark_methods():
    print("\nEXPERIMENTAL TIMINGS")

    for n in (365, 36_500, 365_000):
        data = [random.randint(0, 100) for _ in range(n)]

        start = time.perf_counter()
        naive_result = naive_moving_average(data)
        naive_time = time.perf_counter() - start

        start = time.perf_counter()
        running_result = running_moving_average(data)
        running_time = time.perf_counter() - start

        equal = all(
            abs(a - b) < 1e-9
            for a, b in zip(naive_result, running_result)
        )

        print(f"\nReadings: {n}")
        print(f"Naive method: {naive_time:.6f} seconds")
        print(f"Running-sum method: {running_time:.6f} seconds")
        print("Results agree:", equal)


# 7. EDGE CASE TESTING

def test_edge_cases():
    print("\nEDGE CASE TESTING")

    empty = []
    short = [10, 20, 30, 40, 50]
    exact = [10, 20, 30, 40, 50, 60, 70]

    print("Empty list:", naive_moving_average(empty))
    print("Empty list running sum:", running_moving_average(empty))

    print("Short list:", naive_moving_average(short))
    print("Short list running sum:", running_moving_average(short))

    print("Exactly seven values:", naive_moving_average(exact))

    try:
        naive_moving_average(exact, 0)
    except ValueError as error:
        print("Invalid window:", error)


# 8. LIST INSERTION COST

def insertion_cost_test():
    print("\nLIST INSERTION COST")

    for n in (365, 36_500, 365_000):
        data = list(range(n))

        start = time.perf_counter()

        for _ in range(20):
            data.insert(0, -1)
            data.pop(0)

        elapsed = time.perf_counter() - start

        print(
            f"List size: {n}, "
            f"20 front insertions and removals: {elapsed:.6f} seconds"
        )

    print("append(): O(1) amortized")
    print("insert(): O(n) at an arbitrary position")
    print("pop() at end: O(1)")
    print("pop() at beginning: O(n)")
    print("sort(): O(n log n)")


# 9. MAIN PROGRAM

def main():
    random.seed(42)

    readings = [
        random.randint(0, 100)
        for _ in range(365)
    ]

    print("=" * 60)
    print("             DAILY RAINFALL RECORDS")
    print("=" * 60)

    # Daily rainfall readings

    print("\nFIRST 14 READINGS")
    print(readings[:14])

    # Weekly rainfall totals

    weekly_totals = []

    for i in range(0, len(readings), 7):
        week = readings[i:i + 7]
        weekly_totals.append(sum(week))

    print("\nWEEKLY TOTALS")
    print(weekly_totals)
    print("Number of weeks:", len(weekly_totals))
    print("Readings in final week:", len(readings[364:]))

    # Wettest and driest weeks

    wettest_week = max(weekly_totals)
    driest_week = min(weekly_totals)

    wettest_week_numbers = [
        i + 1 for i, total in enumerate(weekly_totals)
        if total == wettest_week
    ]

    driest_week_numbers = [
        i + 1 for i, total in enumerate(weekly_totals)
        if total == driest_week
    ]

    print("\nWETTEST AND DRIEST WEEKS")
    print("Wettest weekly rainfall:", wettest_week, "mm")
    print("Wettest week number(s):", wettest_week_numbers)
    print("Driest weekly rainfall:", driest_week, "mm")
    print("Driest week number(s):", driest_week_numbers)

    # Maximum and minimum daily rainfall

    maximum = max(readings)
    minimum = min(readings)

    maximum_days = [
        i + 1 for i, value in enumerate(readings)
        if value == maximum
    ]

    minimum_days = [
        i + 1 for i, value in enumerate(readings)
        if value == minimum
    ]

    print("\nDAILY MAXIMUM AND MINIMUM")
    print("Maximum rainfall:", maximum, "mm")
    print("Maximum rainfall day(s):", maximum_days)
    print("Minimum rainfall:", minimum, "mm")
    print("Minimum rainfall day(s):", minimum_days)

    # Seven-day moving averages

    naive = naive_moving_average(readings)
    running = running_moving_average(readings)

    print("\n7-DAY MOVING AVERAGE")
    print("First 10 naive averages:", [round(x, 2) for x in naive[:10]])
    print("First 10 running averages:", [round(x, 2) for x in running[:10]])

    methods_agree = all(
        abs(a - b) < 1e-9
        for a, b in zip(naive, running)
    )

    print("Both methods agree:", methods_agree)
    print("Total moving averages:", len(naive))

    # Dry days

    dry_days = [
        i + 1 for i, value in enumerate(readings)
        if value == 0
    ]

    print("\nDRY DAYS")
    print("Days with zero rainfall:", dry_days)
    print("Total dry days:", len(dry_days))

    # Slicing demonstrations

    print("\nLIST SLICING")

    print("readings[7:14]:", readings[7:14])
    print("readings[-7:]:", readings[-7:])
    print("readings[::7]:", readings[::7])

    print("\nSLICING EXPLANATION")
    print("readings[7:14] returns elements at indexes 7 to 13.")
    print("readings[-7:] returns the last seven readings.")
    print("readings[::7] returns every seventh reading from index 0.")
    print("readings[::7] does not calculate weekly totals.")

    # List operations

    print("\nLIST OPERATIONS")

    sample = [10, 20, 30, 40]

    sample.append(50)
    print("After append:", sample)

    sample.insert(1, 15)
    print("After insert:", sample)

    sample.pop()
    print("After pop:", sample)

    sample.sort()
    print("After sort:", sample)

    # Operation counts

    print("\nOPERATION COUNT COMPARISON")

    for n in (365, 36_500, 365_000):
        compare_operation_counts(n)

    # Performance benchmark

    benchmark_methods()

    # Edge cases

    test_edge_cases()

    # Insertion cost

    insertion_cost_test()

    # Deque alternative

    print("\nDEQUE ALTERNATIVE")

    deque_result = deque_moving_average(readings)

    deque_agrees = all(
        abs(a - b) < 1e-9
        for a, b in zip(naive, deque_result)
    )

    print("Deque results agree:", deque_agrees)
    print("First 10 deque averages:", [round(x, 2) for x in deque_result[:10]])
    print("Deque window storage: O(7) = O(1)")
    print("Deque moving average using sum per window: O(7n)")

    # Dictionary alternative

    print("\nDICTIONARY ALTERNATIVE")

    rainfall_by_date, dictionary_averages = (
        dictionary_moving_average(readings)
    )

    print("Number of date records:", len(rainfall_by_date))
    print("First date:", min(rainfall_by_date))
    print("Last date:", max(rainfall_by_date))
    print("First date rainfall:", rainfall_by_date[min(rainfall_by_date)])
    print("Dictionary moving averages agree:", all(
        abs(a - b) < 1e-9
        for a, b in zip(naive, dictionary_averages)
    ))

    # Complexity analysis

    print("\nCOMPLEXITY ANALYSIS")
    print("Weekly totals: O(n) time")
    print("Maximum and minimum: O(n) time")
    print("Naive moving average: O(7n) time")
    print("Running-sum moving average: O(n) time")
    print("Deque window storage: O(7) = O(1) space")
    print("Dictionary storage: O(n) space")
    print("List insertion at beginning: O(n) time")
    print("Dictionary average lookup: O(1)")

    print("\n" + "=" * 60)
    print("                 TASK 01 COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()