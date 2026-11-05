
import re
import time


# Normalize phone number
def normalize_phone(phone):
    digits = re.sub(r"\D", "", str(phone))

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]

    return digits


# Normalize email
def normalize_email(email):
    return str(email).strip().lower()


# Merge duplicate contacts
def merge_contacts(contacts):
    parent = list(range(len(contacts)))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    phone_index = {}
    email_index = {}
    records = []

    for i, contact in enumerate(contacts):
        phones = contact.get("phones", contact.get("phone", []))
        emails = contact.get("emails", contact.get("email", []))

        if isinstance(phones, (str, int)):
            phones = [phones]
        if isinstance(emails, str):
            emails = [emails]

        phones = {
            normalize_phone(p) for p in phones
            if p is not None and normalize_phone(p)
        }

        emails = {
            normalize_email(e) for e in emails
            if e is not None and normalize_email(e)
        }

        records.append({
            "name": str(contact.get("name", "")).strip(),
            "phones": phones,
            "emails": emails
        })

        for phone in phones:
            if phone in phone_index:
                union(i, phone_index[phone])
            else:
                phone_index[phone] = i

        for email in emails:
            if email in email_index:
                union(i, email_index[email])
            else:
                email_index[email] = i

    merged = {}

    for i, record in enumerate(records):
        root = find(i)

        if root not in merged:
            merged[root] = {
                "names": set(),
                "phones": set(),
                "emails": set()
            }

        if record["name"]:
            merged[root]["names"].add(record["name"])

        merged[root]["phones"].update(record["phones"])
        merged[root]["emails"].update(record["emails"])

    result = {}

    for i, contact in enumerate(merged.values(), start=1):
        phones = sorted(contact["phones"])
        emails = sorted(contact["emails"])
        names = sorted(contact["names"])

        key = phones[0] if phones else f"NO_PHONE_{i}"

        result[key] = {
            "name": names[0] if names else "Unknown",
            "phones": phones,
            "emails": emails
        }

    return result


# Sample contacts
def sample_contacts():
    return [
        {"name": "Alice", "phone": "+91 98765-43210",
         "email": "ALICE@gmail.com"},

        {"name": "Alice Johnson", "phone": "09876543210",
         "email": "alice@gmail.com"},

        {"name": "Bob", "phone": "9123456789",
         "email": "bob@gmail.com"},

        {"name": "Bob Kumar", "phone": "9123456789",
         "email": "bob.work@gmail.com"},

        {"name": "Charlie", "phone": "9988776655",
         "email": "charlie@gmail.com"},

        {"name": "David", "email": "david@gmail.com"},

        {"name": "David", "email": "DAVID@gmail.com"},

        {"name": "Alex", "phone": "9000011111"},
        {"name": "Alex", "phone": "9000022222"}
    ]


# Test cases
def test_cases():
    print("\n--- TEST CASES ---")

    print("Phone normalization:",
          normalize_phone("+91 98765-43210") ==
          normalize_phone("09876543210"))

    print("Email normalization:",
          normalize_email("TEST@GMAIL.COM") ==
          normalize_email("test@gmail.com"))

    print("Empty input:", merge_contacts([]))

    same_name = [
        {"name": "Alex", "phone": "9000011111"},
        {"name": "Alex", "phone": "9000022222"}
    ]

    print("Same name, different people:",
          len(merge_contacts(same_name)) == 2)

    missing_phone = [
        {"name": "John", "email": "john@gmail.com"},
        {"name": "John Updated", "email": "JOHN@gmail.com"}
    ]

    print("Missing phone matching:",
          len(merge_contacts(missing_phone)) == 1)


# Performance benchmark
def benchmark():
    print("\n--- PERFORMANCE BENCHMARK ---")

    for size in [1000, 100000]:
        contacts = []

        for i in range(size):
            group = i // 2

            contacts.append({
                "name": f"Person {i}",
                "phone": str(9000000000 + group),
                "email": f"person{group}@gmail.com"
            })

        start = time.perf_counter()
        result = merge_contacts(contacts)
        elapsed = time.perf_counter() - start

        print(f"Input contacts: {size}")
        print(f"Merged contacts: {len(result)}")
        print(f"Execution time: {elapsed:.6f} seconds")


# Main program
def main():
    print("CONTACT MERGING SYSTEM")

    contacts = sample_contacts()

    print("\nOriginal contacts:")
    for contact in contacts:
        print(contact)

    result = merge_contacts(contacts)

    print("\nMerged contacts:")
    for key, contact in result.items():
        print("\nPrimary key:", key)
        print("Name:", contact["name"])
        print("Phones:", contact["phones"])
        print("Emails:", contact["emails"])

    print("\nOriginal records:", len(contacts))
    print("Merged contacts:", len(result))

    test_cases()
    benchmark()

    print("\nTASK 07 COMPLETED")


if __name__ == "__main__":
    main()
