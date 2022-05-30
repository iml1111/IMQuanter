

class IncomeStatementScraper:

    def __init__(self):
        self.url = 'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp'
        self.params = {
            'pGB': 1,
            'gicode': "A%s", #종목
            'cID': '',
            'MenuYn': 'Y',
            'ReportGB': '%s', #B 별도 < D 연결
            'NewMenuID': 103,
            'stkGb': 701,
        }