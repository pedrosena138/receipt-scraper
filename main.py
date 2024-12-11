import sys

from src.jobs import get_receipt_url, get_receipt_xml


def main():
    try:
        key = "26241206057223051590650110000386551110535440"  # 2624 1293 2097 6506 9400 6551 6000 0032 1710 4857 9174
        # url = "https://nfce.sefaz.pe.gov.br/nfce-web/consNfce?tp=C&chave=26241206057223051590650110000386551110535440&hash=63eff069ba314b97163bc9b4ab60aef7"
        url = get_receipt_url(key)
        get_receipt_xml(url)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
