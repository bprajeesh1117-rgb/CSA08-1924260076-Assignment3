"""Q4 – Sets: Elective Registration Clash Detection."""
import random
import time


def main():
    ai_elective = {"192311001", "192311004", "192311007", "192311009"}
    iot_elective = {"192311002", "192311004", "192311009", "192311010"}
    all_students = {f"1923110{i:02d}" for i in range(1, 11)}

    # Set operators only, as required by Complete the Code.
    both = ai_elective & iot_elective
    exactly_one = ai_elective ^ iot_elective
    neither = all_students - (ai_elective | iot_elective)

    print("clash      :", sorted(both))
    print("exactly one:", sorted(exactly_one))
    print("neither    :", sorted(neither))

    # Same result using set methods.
    both_method = ai_elective.intersection(iot_elective)
    exactly_one_method = ai_elective.symmetric_difference(iot_elective)
    neither_method = all_students.difference(ai_elective.union(iot_elective))
    print("Methods give same results:",
          both == both_method and exactly_one == exactly_one_method
          and neither == neither_method)

    # Duplicate registrations are automatically removed.
    registrations = ["S01", "S02", "S01", "S03", "S02"]
    print("List with duplicates:", registrations)
    print("Set without duplicates:", set(registrations))

    # Membership timing and common-student timing.
    print("\nEXPERIMENTAL INVESTIGATION")
    for n in (10_000, 100_000, 1_000_000):
        data = list(range(n))
        data_set = set(data)
        target = n - 1

        start = time.perf_counter()
        _ = target in data
        list_time = time.perf_counter() - start

        start = time.perf_counter()
        _ = target in data_set
        set_time = time.perf_counter() - start

        print(f"n={n}: list membership={list_time:.9f}s, "
              f"set membership={set_time:.9f}s")

    list_a = list(range(0, 5000))
    list_b = list(range(2500, 7500))
    start = time.perf_counter()
    common_nested = [x for x in list_a for y in list_b if x == y]
    nested_time = time.perf_counter() - start
    start = time.perf_counter()
    common_set = set(list_a) & set(list_b)
    operator_time = time.perf_counter() - start
    print("Nested-loop common count:", len(common_nested))
    print("Set intersection common count:", len(common_set))
    print("Nested-loop time:", round(nested_time, 6), "seconds")
    print("Set intersection time:", round(operator_time, 6), "seconds")

    # Empty and identical elective tests.
    print("Empty electives:", set() & set(), set() ^ set())
    print("Identical electives:", ai_elective & ai_elective,
          ai_elective ^ ai_elective)


if __name__ == "__main__":
    main()
