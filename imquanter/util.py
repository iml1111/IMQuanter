from datetime import datetime
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
    print('\n[IMQuanter]', *args)


def get_quarter(date_str: str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    div, _ = divmod(date.month - 1, 3)
    return f"Q{div + 1}"


def get_quarter_sequence(start_date: str, end_date: str):
    year = int(start_date[:4])
    quarter = int(get_quarter(start_date)[1:])
    end_year = int(end_date[:4])
    end_quarter = int(get_quarter(end_date)[1:])
    sequence = []
    while (year, quarter) <= (end_year, end_quarter):
        sequence.append((str(year), f'Q{quarter}'))
        if quarter < 4:
            quarter += 1
        else:
            year += 1
            quarter = 1
    return sequence


def now_date():
    return datetime.now().strftime('%Y-%m-%d')


if __name__ == '__main__':
    print(get_quarter_sequence('2020-03-01', '2020-12-01'))
