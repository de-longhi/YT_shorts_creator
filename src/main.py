from facts_collector import facts_collector
from config import API_NINJAS_KEY

FACTS_LIMIT = 1
API_URL = f"https://api.api-ninjas.com/v1/facts"


def main():
    # Fetch facts (e.g., 3 facts)

    scientist = facts_collector.scientist(API_URL, API_NINJAS_KEY, debug=True)
    facts = scientist.fetch()
    if facts:
        print("Interesting Facts:")
        for i, fact in enumerate(facts, start=1):
            print(fact)
    else:
        print("Failed to fetch facts.")


if __name__ == "__main__":
    main()
