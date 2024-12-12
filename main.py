import sys

from src.jobs import get_receipt_url, get_receipt_xml


def main():
    try:
        assert len(sys.argv) > 1, "Argument missing 'key'"
        assert len(sys.argv) < 2, "Too many arguments"

        key = sys.argv[1]
        url = get_receipt_url(key)
        get_receipt_xml(url, key)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
