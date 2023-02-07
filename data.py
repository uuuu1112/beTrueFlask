from basic import *
import concurrent.futures
import re

# 這個class，我想拿到特定公司的基礎資料
class API(FromAPI):
    def __init__(self,stock_id):
        super().__init__()    
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
    # 同時呼叫基本的api，並且把值存在table
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
# 處理頁面要的資料
class ManageData(FromAPI):
    def __init__(self):
        super().__init__()
    def getPiovotTable(self,table,values,columns='stock_id',index='date'):
        return table.pivot_table(index=index,values=values,columns=columns)
    def cleanSeason(self,year):
        if re.search('年',year):
            pos=re.search('年',year).start()
            return year[:pos]
        else:
            return year    
    def priceContent(self,table,values='close',columns='stock_id',index='date'):
        pivotTable=self.getPiovotTable(table,values,columns,index)
        return pivotTable.reset_index()
    def revenueContent(self,table,values='revenue',columns='stock_id',index='date'):
        pivotTable=self.getPiovotTable(table,values,columns,index)
        return pivotTable.reset_index()
    def financialContent(self,table,values='value',columns='type',index='date'):
        pivotTable=self.getPiovotTable(table,values,columns,index)
        return pivotTable.reset_index()
    def dividendContent(self,table):
        dividend=table[['year','StockEarningsDistribution','CashEarningsDistribution']]
        dividend['year']=dividend['year'].apply(self.cleanSeason)
        return dividend.groupby('year').sum().sort_index(ascending=False).reset_index() 

# 頁面要用的資料總結
class BasicTable(API):
    def __init__(self,stock_id):
        super().__init__(stock_id) 
        self.dayDates=self.columnList(self.priceTable)
        self.monthDates=self.columnList(self.revenueTable)
        self.seasonDates=self.columnList(self.financialTable)
        self.md=ManageData()
    def columnList(self,table,columnName='date'):
        return list(table[columnName])   
    def allContent(self):
        priceContent=self.md.priceContent(self.priceTable).to_json()
        revenueContent=self.md.revenueContent(self.revenueTable).to_json()
        financialContent=self.md.financialContent(self.financialTable).to_json()
        dividendContent=self.md.dividendContent(self.dividendTable).to_json()
        allContent={'priceTable':priceContent,'revenueTable':revenueContent,'financialTable':financialContent,'dividendTable':dividendContent}
        return allContent
