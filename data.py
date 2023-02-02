from basic import *
import threading

class API(FromAPI):
    def __init__(self,stock_id):
        super().__init__()    
        self.dm=DateManage()
        self.start_date="2000-01-01"
        self.today=self.dm.transToString(self.dm.todayDate())
        self.stock_id=stock_id
        self.revenueTable=pd.DataFrame([])
        self.priceTable=pd.DataFrame([])
        self.financialTable=pd.DataFrame([])
        self.dividendTable=pd.DataFrame([])
    def revenueApi(self):
        return self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockMonthRevenue")
    def priceApi(self):
        return self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockPrice")    
    def financialApi(self):
        return self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockFinancialStatements")    
    def dividendApi(self):
        return self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockDividend")