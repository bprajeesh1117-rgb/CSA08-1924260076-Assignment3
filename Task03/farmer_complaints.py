
import random
import re
import time
from collections import Counter, defaultdict


# Stop words to ignore during complaint analysis
STOP_WORDS = {
    "the", "is", "a", "an", "and", "or", "to",
    "of", "in", "for", "on", "with", "my", "i"
}


# TODO 1: Count word frequencies using dictionary get()
def frequencies(texts, stop):
    counts = {}

    for text in texts:
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

        for word in words:
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1

    return counts


# TODO 2: Return top k words by count, then alphabetically
def top(counts, k):
    return sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )[:k]


# Demonstrate get() and setdefault()
def demonstrate_dictionary_methods():
    print("\n--- DICTIONARY METHODS ---")

    counts = {}

    words = ["seeds", "price", "seeds", "water", "price", "seeds"]

    for word in words:
        counts[word] = counts.get(word, 0) + 1

    print("Using get():", counts)

    district_complaints = {}
    complaints = [
        ("Chennai", "Seed quality is poor"),
        ("Madurai", "Water supply problem"),
        ("Chennai", "Fertilizer price is high")
    ]

    for district, complaint in complaints:
        district_complaints.setdefault(district, []).append(complaint)

    print("Using setdefault():")
    for district, items in district_complaints.items():
        print(district, ":", items)


# Group complaints by district
def group_by_district(complaints):
    district_groups = {}

    for district, complaint in complaints:
        district_groups.setdefault(district, []).append(complaint)

    return district_groups


# Generate sample complaints
def generate_complaints(number):
    topics = [
        "seeds quality is poor",
        "fertilizer price is high",
        "water supply is not received",
        "crop damage due to insects",
        "subsidy payment is delayed",
        "electricity supply is irregular",
        "market price is low"
    ]

    districts = [
        "Chennai", "Madurai", "Coimbatore",
        "Salem", "Trichy"
    ]

    data = []

    for i in range(number):
        complaint = topics[i % len(topics)]
        district = districts[i % len(districts)]
        data.append((district, complaint))

    return data


# Compare dictionary, list.count(), and Counter
def benchmark_methods(number):
    print(f"\n--- BENCHMARK: {number:,} COMPLAINTS ---")

    data = generate_complaints(number)
    texts = [complaint for district, complaint in data]

    # Dictionary frequency counting
    start = time.perf_counter()
    dictionary_counts = frequencies(texts, STOP_WORDS)
    dictionary_time = time.perf_counter() - start

    # Counter frequency counting
    start = time.perf_counter()
    all_words = []

    for text in texts:
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
        all_words.extend(
            word for word in words if word not in STOP_WORDS
        )

    counter_counts = Counter(all_words)
    counter_time = time.perf_counter() - start

    # list.count() frequency counting
    start = time.perf_counter()
    unique_words = set(all_words)
    list_counts = {
        word: all_words.count(word)
        for word in unique_words
    }
    list_time = time.perf_counter() - start

    print(f"Dictionary time: {dictionary_time:.6f} seconds")
    print(f"Counter time:    {counter_time:.6f} seconds")
    print(f"list.count time: {list_time:.6f} seconds")

    print("Dictionary and Counter agree:",
          dictionary_counts == dict(counter_counts))
    print("Dictionary and list.count agree:",
          dictionary_counts == list_counts)


# Test empty, uppercase, and punctuation cases
def test_cases():
    print("\n--- TEST CASES ---")

    print("Empty input:", frequencies([], STOP_WORDS))

    test_texts = [
        "SEEDS are poor!",
        "Seeds are expensive.",
        "PRICE is HIGH!!!"
    ]

    result = frequencies(test_texts, STOP_WORDS)
    print("Case and punctuation test:", result)
    print("Top 3:", top(result, 3))


# Demonstrate dictionary insertion order and views
def demonstrate_dictionary_features():
    print("\n--- DICTIONARY FEATURES ---")

    sample = {
        "seeds": 3,
        "price": 2,
        "received": 2
    }

    print("Keys:", sample.keys())
    print("Values:", sample.values())
    print("Items:", sample.items())

    print("Insertion order:", list(sample.keys()))


# Main program
def main():
    print("FARMER HELPLINE COMPLAINT ANALYSIS")

    demonstrate_dictionary_methods()
    demonstrate_dictionary_features()

    complaints = [
        ("Chennai", "Seeds are poor and seeds are expensive"),
        ("Madurai", "Price is high and water is not received"),
        ("Chennai", "Seeds quality is poor"),
        ("Coimbatore", "Price is high")
    ]

    print("\n--- COMPLAINT ANALYSIS ---")

    texts = [complaint for district, complaint in complaints]

    word_counts = frequencies(texts, STOP_WORDS)

    print("Word frequencies:")
    for word, count in sorted(word_counts.items()):
        print(f"{word}: {count}")

    print("\nTop 5 words:")
    print(top(word_counts, 5))

    print("\n--- DISTRICT-WISE COMPLAINTS ---")

    district_data = group_by_district(complaints)

    for district, items in district_data.items():
        print(f"\n{district}:")
        for complaint in items:
            print("-", complaint)

    test_cases()

    print("\n--- PERFORMANCE COMPARISON ---")
    for size in [1000, 10000, 100000]:
        benchmark_methods(size)

    print("\n--- EXPECTED TOP FUNCTION TEST ---")
    expected = {
        "seeds": 3,
        "price": 2,
        "received": 2
    }

    print(top(expected, 3))
    # Expected:
    # [('seeds', 3), ('price', 2), ('received', 2)]


if __name__ == "__main__":
    main()
