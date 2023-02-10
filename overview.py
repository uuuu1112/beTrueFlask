from basic import *

class OverviewContent(FromAPI):
    def __init__(self):
        super().__init__()
    def revenueApi(self,date):
        return self.multiStock(date,"TaiwanStockMonthRevenue")

class OverviewTable(OverviewContent):
    def __init__(self):
        super().__init__()
    def allContent(self,monthDate):
        return self.revenueApi(monthDate).to_json()
        