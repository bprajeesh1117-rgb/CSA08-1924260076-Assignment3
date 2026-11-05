"""Q7 – Design a Contact-Merging Program from First Principles."""
import random
import re
import time


CONTACTS_PHONE_1 = [
    {"name": "Dr. Ravi", "phone": "+91 98400 12345", "email": "ravi@example.com"},
    {"name": "Anu", "phone": "98765 43210", "email": "anu@example.com"},
]
CONTACTS_PHONE_2 = [
    {"name": "ravi kumar", "phone": "9840012345", "email": "r.kumar@example.com"},
    {"name": "Karthik", "phone": "+91-90000-11111", "email": ""},
]
SIM_CONTACTS = [
    {"name": "Ravi", "phone": "09840012345", "email": "ravi.work@example.com"},
    {"name": "Meena", "phone": "", "email": "meena@example.com"},
]


def normalize_phone(phone):
    """Keep digits only and remove India's country code or trunk prefix."""
    digits = re.sub(r"\D", "", phone or "")
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 11:
        digits = digits[1:]
    return digits


def normalize_name(name):
    return " ".join((name or "").lower().strip().split())


def merge_contacts(contact_lists):
    """Group contacts by normalized phone; retain names, numbers and emails."""
    merged = {}
    no_phone = []

    for contacts in contact_lists:
        for contact in contacts:
            normalized = normalize_phone(contact.get("phone", ""))
            if not normalized:
                no_phone.append({
                    "names": {contact.get("name", "").strip()} - {""},
                    "numbers": set(),
                    "emails": {contact.get("email", "").strip()} - {""},
                })
                continue

            if normalized not in merged:
                merged[normalized] = {
                    "names": set(),
                    "numbers": set(),
                    "emails": set(),
                }

            name = contact.get("name", "").strip()
            phone = contact.get("phone", "").strip()
            email = contact.get("email", "").strip()

            if name:
                merged[normalized]["names"].add(name)
            if phone:
                merged[normalized]["numbers"].add(phone)
            if email:
                merged[normalized]["emails"].add(email)

    return list(merged.values()) + no_phone


def pairwise_duplicate_groups(contacts):
    """Alternative O(n^2) comparison by normalized phone."""
    groups = []
    used = set()
    for i, contact in enumerate(contacts):
        if i in used:
            continue
        key = normalize_phone(contact.get("phone", ""))
        if not key:
            continue
        group = [contact]
        used.add(i)
        for j in range(i + 1, len(contacts)):
            if j not in used and normalize_phone(contacts[j].get("phone", "")) == key:
                group.append(contacts[j])
                used.add(j)
        groups.append(group)
    return groups


def main():
    sources = [CONTACTS_PHONE_1, CONTACTS_PHONE_2, SIM_CONTACTS]
    merged = merge_contacts(sources)

    print("MERGED CONTACTS")
    for number, contact in enumerate(merged, start=1):
        print(f"{number}. Names: {sorted(contact['names'])}")
        print("   Numbers:", sorted(contact["numbers"]))
        print("   Emails:", sorted(contact["emails"]))

    # Hand-checkable duplicate test.
    small = [
        [{"name": "Dr. Ravi", "phone": "+91 98400 12345",
          "email": "ravi@example.com"}],
        [{"name": "ravi kumar", "phone": "9840012345",
          "email": "rk@example.com"}],
    ]
    small_result = merge_contacts(small)
    print("\nSMALL TEST: expected one Ravi contact; actual groups:", len(small_result))
    print("Small test result:", small_result)

    print("\nEXPERIMENTAL TIMINGS")
    for n in (1_000, 100_000):
        contacts = []
        for i in range(n):
            phone_number = f"9{i % max(1, n // 2):09d}"[-10:]
            contacts.append({
                "name": f"Person {i}",
                "phone": phone_number,
                "email": f"person{i}@example.com",
            })

        start = time.perf_counter()
        dictionary_result = merge_contacts([contacts])
        dict_time = time.perf_counter() - start

        start = time.perf_counter()
        pairwise_result = pairwise_duplicate_groups(contacts[:1000])
        pairwise_time = time.perf_counter() - start

        print(f"n={n}: dictionary merge={dict_time:.6f}s")
        if n == 1_000:
            print(f"n=1000: pairwise comparison={pairwise_time:.6f}s")
        else:
            print("Pairwise comparison not run for 100,000 contacts because "
                  "quadratic work is impractical; 1,000-contact timing is shown.")
        print("Dictionary groups:", len(dictionary_result))

    print("\nLIMITATION")
    print("Contacts without a phone number cannot reliably be matched by this "
          "phone-keyed design. They are retained separately for manual review.")


if __name__ == "__main__":
    main()
