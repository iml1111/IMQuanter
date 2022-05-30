import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import MySQLdb
from tqdm import tqdm
from sqlalchemy import create_engine


def get_IS(code='005930', gb='D'):
    URL = 'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp'
    params = {
        'pGB': 1,
        'gicode': "A%s" % code,  # 종목
        'cID': '',
        'MenuYn': 'Y',
        'ReportGB': gb,  # B 별도 < D 연결
        'NewMenuID': 103,
        'stkGb': 701,
    }
    res = requests.get(URL, params=params)
    soup = bs(res.text, 'html.parser')

    years = soup.select_one('div#divSonikY')
    quaters = soup.select_one('div#divSonikQ')
    soups = [('Y', years), ('Q', quaters)]

    report = []
    for term, soup in soups:
        # 연도/분기 데이터 추출
        terms = soup.select('thead > tr > th')
        terms = [i.get_text().strip() for i in terms][1:-2]
        # 연도별일 경우, 마지막 /12 부분 제거
        if term == 'Y':
            terms = [i[:-3] for i in terms]

        # 손익계산서 칼럼 추출
        cols = soup.select('tbody > tr > th')
        cols = [
            i.get_text().strip() \
                .replace('\xa0', '').replace('계산에 참여한 계정 펼치기', '')
            for i in cols
        ]

        # 손익계산서 데이터 2차원 배열 형태로 추출
        array = []
        trs = soup.select('tbody > tr')
        for tr in trs:
            tds = tr.select('td')
            refined = []
            for td in tds:
                # 가능하다면 title에서 추출.
                if td.get('title'):
                    temp = td.get('title').strip()
                elif td.get_text().strip():
                    temp = td.get_text().strip()
                else:
                    temp = None
                refined.append(temp)
            array.append(refined)

        # 연간/분기순으로 순회하며 데이터 가공 및 반환
        for idx, term_i in enumerate(terms):
            record = {
                'stock_code': code,
                'period': term_i,
            }
            for jdx, col in enumerate(cols):
                if array[jdx][idx]:
                    record[col] = float(array[jdx][idx].replace(',', ''))
                else:
                    record[col] = np.NaN

            record.pop('영업이익(발표기준)', None)
            if not record.get('지배주주순이익'):
                record['지배주주순이익'] = np.NaN
            if not record.get('비지배주주순이익'):
                record['비지배주주순이익'] = np.NaN
            report.append(record)

    return report


def sampling(report):
    sampled = []
    for data in report:
        sampled.append({
            'stock_code': data['stock_code'],
            'period': data['period'],
            'Revenue': data['매출액'],
            'Cost_Sales': data['매출원가'],
            'Gross_Profit': data['매출총이익'],
            'Sale_Admin_Total': data['판매비와관리비'],
            'Sale_Exp': data['판매비'],
            'Admin_Exp': data['관리비'],
            'financial_income': data['금융수익'],
            'interest_income': data['이자수익'],
            'Reversal_of_allowance': data['대손충당금환입액'],
            'Profits_trade_receivables': data['매출채권처분이익'],
            'Pre-tax_profit_business': data['세전계속사업이익'],
            'Net_Income': data['당기순이익'],
            'Net_Income1': data['지배주주순이익'],
            'Net_Income2': data['비지배주주순이익'],
        })
    return sampled


if __name__ == '__main__':
    db = MySQLdb.connect(user="root", passwd="hkw10256", db="my1st_db")
    c = db.cursor()

    # 이전 강의에서 추출했던 stock_code 호출
    c.execute('SELECT stock_code FROM korea_stock')
    codes = [i[0] for i in c.fetchall()]

    total_report = []
    for code in tqdm(codes):
        report = get_IS(code=code)
        try:
            """
            일부 필드만 샘플링하는 과정 중, Key Error 발생.
            몇몇 종목의 손익계산서의 필드 형태라 다른 것으로 추측.
            """
            report = sampling(report)
        except:
            continue
        total_report.extend(report)

    df = pd.DataFrame(total_report)
    server = '127.0.0.1'  # local server
    user = 'root'  # user name
    password = 'hkw10256'  # 개인 password
    db = 'my1st_db'  # DB 이름

    # sqlalchemy의 create_engine을 이용해 DB 연결
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(user, password, server, db))
    df.to_sql(
        name='korea_IS',
        con=engine,
        if_exists='replace',
        index=False,
    )
    c.close()
    """
    mysql> select stock_code, period, Revenue, Gross_Profit from korea_IS limit 10;
    +------------+---------+------------+--------------+
    | stock_code | period  | Revenue    | Gross_Profit |
    +------------+---------+------------+--------------+
    | 005930     | 2018    | 2437714.15 |   1113770.04 |
    | 005930     | 2019    | 2304008.81 |    831613.32 |
    | 005930     | 2020    | 2368069.88 |    923186.92 |
    | 005930     | 2021    | 2796047.99 |   1131934.57 |
    | 005930     | 2021/03 |  653885.03 |    238885.18 |
    | 005930     | 2021/06 |  636715.85 |    266056.54 |
    | 005930     | 2021/09 |  739791.87 |    310803.16 |
    | 005930     | 2021/12 |  765655.24 |    316189.69 |
    | 373220     | 2018    |       NULL |         NULL |
    | 373220     | 2019    |       NULL |         NULL |
    +------------+---------+------------+--------------+
    """