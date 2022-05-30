import FinanceDataReader as fdr


def get_all_kospi(dry=True):
    """
    # KOSPI 주식 종목 코드 리스트 반환
    :param dry: 테스트 실행 여부
    :return: 코드 리스트 반환
    - stocks: (
        Symbol, Market, Name,Sector, Industry,
        ListingDate, SettleMonth, Representative,
        HomePage, Region)
    """
    if dry:
        return [
            '005930', # 삼성전자
            '066570', # 엘지전자
        ]
    # All KOSPI Symbols
    stocks = fdr.StockListing('KOSPI')
    stocks: dict = stocks.to_dict(orient='index')
    results = []
    for record in stocks.values():
        results.append(record['Symbol'])
    return results


def log(*args):
    print('[IMQuanter]', *args)


if __name__ == '__main__':
    print(get_all_kospi())