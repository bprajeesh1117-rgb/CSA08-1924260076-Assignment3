"""Q6 – Nested Data: A Railway Timetable."""
import random
import time
import sys
from collections import defaultdict


def build_timetable():
    return {
        "12601": {
            "name": "Chennai Mail",
            "stops": [("Chennai", "06:00", "06:10"),
                      ("Vijayawada", "12:00", "12:05"),
                      ("Howrah", "08:00", "08:10")],
            "days": {"Mon", "Wed", "Fri"},
        },
        "12602": {
            "name": "Kaveri Express",
            "stops": [("Chennai", "07:00", "07:15"),
                      ("Bengaluru", "12:00", "12:10"),
                      ("Mysuru", "14:00", "14:10")],
            "days": {"Tue", "Thu", "Sat"},
        },
        "12603": {
            "name": "Vaigai Express",
            "stops": [("Chennai", "13:00", "13:10"),
                      ("Madurai", "20:00", "20:10")],
            "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat"},
        },
        "12604": {
            "name": "Pandian Express",
            "stops": [("Chennai", "21:00", "21:15"),
                      ("Madurai", "05:00", "05:10")],
            "days": {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"},
        },
        "12605": {
            "name": "West Coast Express",
            "stops": [("Chennai", "11:00", "11:10"),
                      ("Coimbatore", "19:00", "19:10")],
            "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"},
        },
    }


def build_station_index(timetable):
    index = defaultdict(list)
    for train_no, details in timetable.items():
        for station, arrival, departure in details["stops"]:
            index[station].append((train_no, arrival, departure))
    return index


def main():
    timetable = build_timetable()
    print("RAILWAY TIMETABLE")
    for train_no, details in timetable.items():
        print(train_no, "-", details["name"], "| Days:", sorted(details["days"]))
        for station, arrival, departure in details["stops"]:
            print("   ", station, "Arrival:", arrival, "Departure:", departure)

    # Find trains stopping at a station on a given day.
    station_query, day_query = "Madurai", "Mon"
    matches = []
    for train_no, details in timetable.items():
        if day_query in details["days"]:
            for station, arrival, departure in details["stops"]:
                if station == station_query:
                    matches.append((train_no, details["name"], departure))
    matches.sort(key=lambda item: item[2])
    print(f"\nTrains at {station_query} on {day_query}:", matches)

    # Example expression for departure from the third stop of a train:
    # timetable["12601"]["stops"][2][2]
    print("Third stop departure of 12601:",
          timetable["12601"]["stops"][2][2])

    # Build station -> train index and query it.
    index = build_station_index(timetable)
    indexed_matches = []
    for train_no, arrival, departure in index.get(station_query, []):
        if day_query in timetable[train_no]["days"]:
            indexed_matches.append((train_no, timetable[train_no]["name"], departure))
    indexed_matches.sort(key=lambda item: item[2])
    print("Indexed query result:", indexed_matches)

    print("Unknown station:", index.get("Atlantis", []))
    print("Train 12602 runs Monday:", "Mon" in timetable["12602"]["days"])

    # Generate synthetic timetables of requested sizes and compare query time.
    print("\nEXPERIMENTAL INVESTIGATION")
    stations = ["Chennai", "Madurai", "Salem", "Trichy", "Coimbatore",
                "Bengaluru", "Vijayawada", "Hyderabad"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for n in (100, 1_000, 10_000):
        generated = {}
        for i in range(n):
            chosen = random.sample(stations, k=4)
            generated[str(10000 + i)] = {
                "name": f"Train-{i}",
                "stops": [(s, "10:00", "10:05") for s in chosen],
                "days": set(random.sample(days, k=5)),
            }

        query = "Chennai"
        start = time.perf_counter()
        plain = []
        for train_no, details in generated.items():
            for station, arrival, departure in details["stops"]:
                if station == query:
                    plain.append(train_no)
        plain_time = time.perf_counter() - start

        start = time.perf_counter()
        generated_index = build_station_index(generated)
        index_build_time = time.perf_counter() - start
        start = time.perf_counter()
        indexed = generated_index.get(query, [])
        indexed_time = time.perf_counter() - start

        print(f"trains={n}: scan={plain_time:.6f}s, "
              f"index_build={index_build_time:.6f}s, "
              f"indexed_lookup={indexed_time:.9f}s, "
              f"matches={len(plain)}, indexed_matches={len(indexed)}")

    print("Approximate index container size (bytes):", sys.getsizeof(index))


if __name__ == "__main__":
    main()
