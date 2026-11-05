"""Q1 – Lists and Slicing: Daily Rainfall Records."""
import random
import time
from collections import deque


def naive_moving_average(values, window=7):
    if len(values) < window:
        return []
    return [sum(values[i:i + window]) / window
            for i in range(len(values) - window + 1)]


def running_moving_average(values, window=7):
    if len(values) < window:
        return []
    result = []
    total = sum(values[:window])
    result.append(total / window)
    for i in range(window, len(values)):
        total += values[i] - values[i - window]
        result.append(total / window)
    return result


def deque_moving_average(values, window=7):
    q = deque(maxlen=window)
    result = []
    for value in values:
        q.append(value)
        if len(q) == window:
            result.append(sum(q) / window)
    return result


def main():
    random.seed(42)
    readings = [random.randint(0, 100) for _ in range(365)]

    print("DAILY RAINFALL RECORDS")
    print("First 14 readings:", readings[:14])

    weekly_totals = [sum(readings[i:i + 7])
                     for i in range(0, len(readings), 7)]
    print("Weekly totals:", weekly_totals)
    print("Number of weekly totals:", len(weekly_totals))

    highest, lowest = max(readings), min(readings)
    print("Maximum rainfall:", highest)
    print("Maximum day(s):", [i + 1 for i, x in enumerate(readings) if x == highest])
    print("Minimum rainfall:", lowest)
    print("Minimum day(s):", [i + 1 for i, x in enumerate(readings) if x == lowest])

    naive = naive_moving_average(readings)
    running = running_moving_average(readings)
    print("First 10 naive moving averages:", [round(x, 2) for x in naive[:10]])
    print("First 10 running-sum averages:", [round(x, 2) for x in running[:10]])
    print("Methods agree:", all(abs(a-b) < 1e-9 for a, b in zip(naive, running)))

    dry_days = [i + 1 for i, x in enumerate(readings) if x == 0]
    print("Dry days (0 mm):", dry_days)

    print("readings[7:14]:", readings[7:14])
    print("readings[-7:]:", readings[-7:])
    print("readings[::7]:", readings[::7])

    print("\nEXPERIMENTAL TIMINGS")
    for n in (365, 36_500, 365_000):
        data = [random.randint(0, 100) for _ in range(n)]
        start = time.perf_counter()
        a = naive_moving_average(data)
        naive_time = time.perf_counter() - start
        start = time.perf_counter()
        b = running_moving_average(data)
        running_time = time.perf_counter() - start
        print(f"n={n}: naive={naive_time:.6f}s, running_sum={running_time:.6f}s, equal={a == b}")

    print("\nEDGE CASES")
    print("Empty list:", naive_moving_average([]), running_moving_average([]))
    short = [10, 20, 30, 40, 50]
    print("Fewer than 7:", naive_moving_average(short), running_moving_average(short))

    print("\nDEQUE ALTERNATIVE")
    print("Deque agrees:", all(abs(a-b) < 1e-9
                               for a, b in zip(naive, deque_moving_average(readings))))
    print("Deque first 10:", [round(x, 2) for x in deque_moving_average(readings)[:10]])


if __name__ == "__main__":
    main()
