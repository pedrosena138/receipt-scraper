import sys

from src.jobs import get_receipt_url, get_receipt_xml


def main():
    try:
        key = "26241293209765069400655160000032171048579174"
        url = get_receipt_url(key)
        get_receipt_xml(url, key)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
