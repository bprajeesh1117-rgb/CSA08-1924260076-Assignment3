"""Q3 – Dictionaries: Farmer Helpline Complaint Analysis."""
import random
import re
import time
from collections import Counter, defaultdict


CALLS = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]
STOP = {"not", "high"}


def frequencies(texts, stop):
    counts = {}
    for text in texts:
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
        for word in words:
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts


def top(counts, k):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]


def main():
    print("FREQUENCIES:", frequencies(CALLS, STOP))
    print("TOP 3:", top(frequencies(CALLS, STOP), 3))

    complaints = [
        {"district": "Chennai", "crop": "rice", "text": "seeds delayed"},
        {"district": "Madurai", "crop": "cotton", "text": "pest attack"},
        {"district": "Chennai", "crop": "rice", "text": "water shortage"},
        {"district": "Salem", "crop": "mango", "text": "fertiliser issue"},
    ]
    by_district = defaultdict(list)
    by_crop = defaultdict(list)
    for complaint in complaints:
        by_district[complaint["district"]].append(complaint["text"])
        by_crop[complaint["crop"]].append(complaint["text"])
    print("COMPLAINTS BY DISTRICT:", dict(by_district))
    print("COMPLAINTS BY CROP:", dict(by_crop))
    print("DISTRICT COUNTS:", {district: len(items)
                               for district, items in by_district.items()})

    print("\nEXPERIMENTAL TIMINGS (synthetic complaint data)")
    vocabulary = ["seeds", "price", "water", "crop", "pest", "fertiliser",
                  "support", "delayed", "received", "damage"]
    for n in (1_000, 10_000, 100_000):
        texts = [" ".join(random.choices(vocabulary, k=12)) for _ in range(n)]

        start = time.perf_counter()
        dictionary_counts = frequencies(texts, set())
        dict_time = time.perf_counter() - start

        all_words = []
        for text in texts:
            all_words.extend(re.findall(r"\b[a-zA-Z]+\b", text.lower()))
        distinct_words = set(all_words)
        start = time.perf_counter()
        list_count_result = {word: all_words.count(word) for word in distinct_words}
        list_count_time = time.perf_counter() - start

        start = time.perf_counter()
        counter_result = Counter(all_words)
        counter_time = time.perf_counter() - start

        print(f"n complaints={n}: dict={dict_time:.6f}s, "
              f"list.count={list_count_time:.6f}s, Counter={counter_time:.6f}s")
        print("Results agree:", dictionary_counts == list_count_result == dict(counter_result))

    print("\nEDGE CASES")
    print("Empty text:", frequencies([""], STOP))
    print("Case and punctuation:", frequencies(["SEEDS, seeds! High."], STOP))


if __name__ == "__main__":
    main()
