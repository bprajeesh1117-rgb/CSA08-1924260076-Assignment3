
import random
import sys
import time

MIN_VALID = -50
MAX_VALID = 50

ALARM_MIN = 2
ALARM_MAX = 8


# 1. Clean sensor readings using a for loop
def clean_with_loop(readings):
    cleaned = []

    for value in readings:
        if MIN_VALID <= value <= MAX_VALID:
            cleaned.append(value)

    return cleaned


# 2. Clean sensor readings using list comprehension
def clean_with_comprehension(readings):
    return [
        value for value in readings
        if MIN_VALID <= value <= MAX_VALID
    ]


# 3. Convert Celsius to Fahrenheit
def celsius_to_fahrenheit(readings):
    return [(value * 9 / 5) + 32 for value in readings]


# 4. Convert Fahrenheit to Celsius
def fahrenheit_to_celsius(readings):
    return [(value - 32) * 5 / 9 for value in readings]


# 5. Detect alarms using enumerate()
# Alarm occurs when temperature is outside 2 to 8.
# The index represents the original minute position.
def detect_alarms(readings):
    alarms = []

    for minute, value in enumerate(readings):
        if value < ALARM_MIN or value > ALARM_MAX:
            alarms.append((minute, value))

    return alarms


# 6. Demonstrate map() and filter()
def demonstrate_map_filter(readings):
    print("\n--- MAP AND FILTER ---")

    fahrenheit = list(
        map(lambda c: (c * 9 / 5) + 32, readings)
    )

    valid = list(
        filter(
            lambda value: MIN_VALID <= value <= MAX_VALID,
            readings
        )
    )

    print("Celsius readings:", readings)
    print("Fahrenheit readings:", [round(x, 2) for x in fahrenheit])
    print("Filtered valid readings:", valid)


# 7. Dictionary and set comprehensions
def demonstrate_comprehensions(readings):
    print("\n--- DICTIONARY AND SET COMPREHENSIONS ---")

    temperature_dictionary = {
        index: value
        for index, value in enumerate(readings)
    }

    unique_readings = {
        value for value in readings
    }

    print("Dictionary comprehension:", temperature_dictionary)
    print("Set comprehension:", unique_readings)


# 8. Generator expression
def generate_valid_readings(readings):
    return (
        value for value in readings
        if MIN_VALID <= value <= MAX_VALID
    )


# 9. Performance comparison
def benchmark():
    print("\n--- PERFORMANCE COMPARISON ---")

    random.seed(42)

    for size in [10_000, 100_000, 1_000_000]:

        readings = [
            random.uniform(-60, 60)
            for _ in range(size)
        ]

        # For loop
        start = time.perf_counter()
        loop_result = clean_with_loop(readings)
        loop_time = time.perf_counter() - start

        # List comprehension
        start = time.perf_counter()
        comprehension_result = clean_with_comprehension(readings)
        comprehension_time = time.perf_counter() - start

        # Map and filter
        start = time.perf_counter()
        map_filter_result = list(
            filter(
                lambda value: MIN_VALID <= value <= MAX_VALID,
                readings
            )
        )
        map_filter_time = time.perf_counter() - start

        # Generator expression
        start = time.perf_counter()
        generator_result = list(generate_valid_readings(readings))
        generator_time = time.perf_counter() - start

        print(f"\nDataset size: {size:,}")
        print(f"For loop: {loop_time:.6f} seconds")
        print(f"List comprehension: {comprehension_time:.6f} seconds")
        print(f"Map/filter: {map_filter_time:.6f} seconds")
        print(f"Generator: {generator_time:.6f} seconds")

        print("Loop and comprehension agree:",
              loop_result == comprehension_result)

        print("Loop and map/filter agree:",
              loop_result == map_filter_result)

        print("Loop and generator agree:",
              loop_result == generator_result)


# 10. Compare memory usage
def compare_memory():
    print("\n--- LIST AND GENERATOR MEMORY ---")

    size = 1_000_000

    list_data = [value for value in range(size)]
    generator_data = (value for value in range(size))

    print("List memory:", sys.getsizeof(list_data), "bytes")
    print("Generator memory:", sys.getsizeof(generator_data), "bytes")

    print("Generator produces values when requested instead of storing them all.")


# 11. Edge case testing
def test_edge_cases():
    print("\n--- EDGE CASE TESTING ---")

    all_valid = [2, 3, 4, 5, 6, 7, 8]
    all_invalid = [-100, -60, 55, 80, 100]

    print("All valid input:", all_valid)
    print("Output:", clean_with_comprehension(all_valid))

    print("\nAll invalid input:", all_invalid)
    print("Output:", clean_with_comprehension(all_invalid))

    print("\nEmpty input:", clean_with_comprehension([]))

    print("\nAlarm test for all-valid input:", detect_alarms(all_valid))
    print("Alarm test for all-invalid input:", detect_alarms(all_invalid))


# 12. Main program
def main():
    print("=" * 55)
    print("SENSOR READING ANALYSIS")
    print("=" * 55)

    readings = [
        25, 30, -55, 45, 60,
        10, 5, 7, 9, -20,
        55, 0, 8, 3, 100
    ]

    print("\nOriginal sensor readings:")
    print(readings)

    # Clean readings
    cleaned = clean_with_loop(readings)

    print("\nCleaned readings (-50 to 50):")
    print(cleaned)

    # Verify list comprehension
    comprehension_result = clean_with_comprehension(readings)

    print("\nList comprehension result:")
    print(comprehension_result)

    print("Both cleaning methods agree:",
          cleaned == comprehension_result)

    # Temperature conversion
    fahrenheit = celsius_to_fahrenheit(cleaned)

    print("\nCelsius readings:")
    print(cleaned)

    print("\nFahrenheit readings:")
    print([round(value, 2) for value in fahrenheit])

    # Convert back
    converted_back = fahrenheit_to_celsius(fahrenheit)

    print("\nConverted back to Celsius:")
    print([round(value, 2) for value in converted_back])

    # IMPORTANT: Use ORIGINAL readings for correct minute positions.
    alarms = detect_alarms(readings)

    print("\nAlarm readings outside 2 to 8:")
    for minute, value in alarms:
        print(f"Minute {minute}: {value}")

    demonstrate_map_filter(cleaned)
    demonstrate_comprehensions(cleaned)

    test_edge_cases()
    compare_memory()
    benchmark()

    print("\n" + "=" * 55)
    print("TASK 05 COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    main()
