"""Q5 – List Comprehension: Cleaning Sensor Readings."""
import random
import sys
import time


def loop_version(readings):
    valid_c = []
    valid_f = []
    for celsius in readings:
        if -50 <= celsius <= 50:
            valid_c.append(celsius)
            valid_f.append((celsius * 9 / 5) + 32)
    return valid_c, valid_f


def comprehension_version(readings):
    valid_c = [c for c in readings if -50 <= c <= 50]
    valid_f = [(c * 9 / 5) + 32 for c in readings if -50 <= c <= 50]
    return valid_c, valid_f


def map_filter_version(readings):
    valid_c = list(filter(lambda c: -50 <= c <= 50, readings))
    valid_f = list(map(lambda c: (c * 9 / 5) + 32, valid_c))
    return valid_c, valid_f


def main():
    readings = [2, 5, 9, -55, 7, 51, 4, 1, 8, -2]
    print("Input readings:", readings)

    valid_c, valid_f = loop_version(readings)
    print("Valid Celsius (loop):", valid_c)
    print("Valid Fahrenheit (loop):", [round(x, 2) for x in valid_f])

    comp_c, comp_f = comprehension_version(readings)
    print("Valid Celsius (comprehension):", comp_c)
    print("Valid Fahrenheit (comprehension):", [round(x, 2) for x in comp_f])

    map_c, map_f = map_filter_version(readings)
    print("Valid Celsius (map/filter):", map_c)
    print("Valid Fahrenheit (map/filter):", [round(x, 2) for x in map_f])
    print("All three versions agree:", valid_c == comp_c == map_c
          and valid_f == comp_f == map_f)

    # enumerate() returns minute positions (starting at minute 1).
    alarm_minutes = [minute for minute, temp in enumerate(readings, start=1)
                     if temp < 2 or temp > 8]
    print("Alarm minutes (outside 2–8 °C):", alarm_minutes)

    # Dictionary and set comprehensions.
    celsius_to_fahrenheit = {c: (c * 9 / 5) + 32 for c in valid_c}
    valid_unique = {c for c in readings if -50 <= c <= 50}
    print("Dictionary comprehension:", celsius_to_fahrenheit)
    print("Set comprehension:", valid_unique)

    print("\nEXPERIMENTAL TIMINGS")
    for n in (10_000, 100_000, 1_000_000):
        data = [random.randint(-60, 60) for _ in range(n)]
        times = []
        outputs = []
        for function in (loop_version, comprehension_version, map_filter_version):
            start = time.perf_counter()
            result = function(data)
            times.append(time.perf_counter() - start)
            outputs.append(result)
        print(f"n={n}: loop={times[0]:.6f}s, "
              f"comprehension={times[1]:.6f}s, map/filter={times[2]:.6f}s")
        print("Results identical:", outputs[0] == outputs[1] == outputs[2])

    # Generator vs list memory (container size only).
    sample = (x for x in range(1_000_000))
    sample_list = [x for x in range(1_000_000)]
    print("List size (bytes):", sys.getsizeof(sample_list))
    print("Generator size (bytes):", sys.getsizeof(sample))

    print("All-valid test:", comprehension_version([2, 3, 4, 5])[0])
    print("All-invalid test:", comprehension_version([51, -51, 60])[0])


if __name__ == "__main__":
    main()
