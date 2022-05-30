import requests
from bs4 import BeautifulSoup as bs


class IncomeStatementScraper:

    def __init__(self):
        self.url = 'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp'

    @staticmethod
    def params(symbol: str, report_gb: str = 'D'):
        return {
            'pGB': 1,
            # 종목
            'gicode': "A%s" % symbol,
            'cID': '',
            'MenuYn': 'Y',
            # B 별도 < D 연결
            'ReportGB': report_gb,
            'NewMenuID': 103,
            'stkGb': 701,
        }

    def get_report(self, symbol: str):
        res = requests.get(
            self.url, params=self.params(symbol))
        soup = bs(rex.text, 'html.parser')
        years = soup.select_one('div#divSonikY')
        quaters = soup.select_one('div#divSonikQ')
        soups = [('Y', years), ('Q', quaters)]