from basic import *
import concurrent.futures
# import threading

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
        self.basicData=self.getBasicData()
    def revenueApi(self):
        self.revenueTable=self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockMonthRevenue")
    def priceApi(self):
        self.priceTable=self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockPrice")    
    def financialApi(self):
        self.financialTable=self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockFinancialStatements")    
    def dividendApi(self):
        self.dividendTable=self.singleStock(self.stock_id,self.start_date,self.today,"TaiwanStockDividend")
    def getBasicData(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_revenue=executor.submit(self.revenueApi)
            future_price=executor.submit(self.priceApi)
            futrue_financial=executor.submit(self.financialApi)
            future_dividend=executor.submit(self.dividendApi)

            future_revenue.result()
            future_price.result()
            futrue_financial.result()
            future_dividend.result()

class BasicTable(API):
    def __init__(self,stock_id):
        super().__init__(stock_id)    