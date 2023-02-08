from basic import *
import concurrent.futures
# import re

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
        self.bt=BasicTrans()
    def priceContent(self,stock_id,table,values='close',columns='stock_id',index='date'):
        pivotTable=self.bt.getPivotTable(table,values,columns,index)
        increase=((pivotTable/self.bt.nShift(1,pivotTable)-1)*100).round(0)
        volume=self.bt.getPivotTable(table,'Trading_Volume',columns,index)
        volumeMean=self.bt.deviationRate(volume,self.bt.periodMean(240,volume))
        monthMean= self.bt.deviationRate(pivotTable,self.bt.periodMean(20,pivotTable))
        seasonMean= self.bt.deviationRate(pivotTable,self.bt.periodMean(60,pivotTable))
        yearMean= self.bt.deviationRate(pivotTable,self.bt.periodMean(240,pivotTable))
        pivotTable.rename(columns={stock_id:'price'},inplace=True)
        increase.rename(columns={stock_id:'increase%'},inplace=True)
        volumeMean.rename(columns={stock_id:'60dayVolDeviation'},inplace=True)
        monthMean.rename(columns={stock_id:'20dayMeanDeviation%'},inplace=True)
        seasonMean.rename(columns={stock_id:'60dayMeanDeviation%'},inplace=True)
        yearMean.rename(columns={stock_id:'240dayMeanDeviation%'},inplace=True)
        dataframe=pivotTable.join(increase)
        dataframe=dataframe.join(volumeMean)
        dataframe=dataframe.join(monthMean)
        dataframe=dataframe.join(seasonMean)
        dataframe=dataframe.join(yearMean)
        dataframe=dataframe.sort_index(ascending=False).reset_index()  
        return dataframe
    def revenueContent(self,stock_id,table,values='revenue',columns='stock_id',index='date'):
        pivotTable=self.bt.getPivotTable(table,values,columns,index)
        YoY=self.bt.periodIncrease(12,pivotTable)
        seasonYoY=self.bt.periodIncrease(12,pivotTable,3)
        yearYoY=self.bt.periodIncrease(12,pivotTable,12)
        year3YoY=self.bt.periodIncrease(36,pivotTable,12)
        year5YoY=self.bt.periodIncrease(60,pivotTable,12)
        YoY.rename(columns={stock_id:'YoY%'},inplace=True)
        seasonYoY.rename(columns={stock_id:'3monthYoY%'},inplace=True)
        yearYoY.rename(columns={stock_id:'12monthYoY%'},inplace=True)  
        year3YoY.rename(columns={stock_id:'12month3yearGrowth%'},inplace=True)
        year5YoY.rename(columns={stock_id:'12month5yearGrowth%'},inplace=True)      
        dataframe=YoY.join(seasonYoY)
        dataframe=dataframe.join(yearYoY)
        dataframe=dataframe.join(year3YoY)
        dataframe=dataframe.join(year5YoY)
        dataframe=dataframe.sort_index(ascending=False).reset_index()  
        return dataframe
    def financialContent(self,table,type='EPS',values='value',columns='type',index='date'):
        pivotTable=self.bt.getPivotTable(table,values,columns,index)[type]
        yearType=self.bt.periodMean(4,pivotTable)
        YoY=self.bt.periodIncrease(4,pivotTable)
        yearYoY=self.bt.periodIncrease(4,yearType)
        dataframe=pd.DataFrame({type:pivotTable,'YoY%':YoY,'year'+type+'YoY%':yearYoY})
        dataframe=dataframe.sort_index(ascending=False).reset_index()
        return dataframe
    def dividendContent(self,table):
        dividend=table[['year','StockEarningsDistribution','CashEarningsDistribution']]
        dividend['year']=dividend['year'].apply(self.bt.cleanSeason)
        dividendTable=dividend.groupby('year').sum().sort_index(ascending=False).reset_index() 
        return dividendTable

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
        priceContent=self.md.priceContent(self.stock_id,self.priceTable).to_json()
        revenueContent=self.md.revenueContent(self.stock_id,self.revenueTable).to_json()
        financialContent=self.md.financialContent(self.financialTable).to_json()
        dividendContent=self.md.dividendContent(self.dividendTable).to_json()
        allContent={'priceTable':priceContent,'revenueTable':revenueContent,'financialTable':financialContent,'dividendTable':dividendContent}
        return allContent
