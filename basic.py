import requests
# import copy
import pandas as pd
from dateManage import *
import re

token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wMi0xMCAyMzowMjowMSIsInVzZXJfaWQiOiJ1dXV1MTExMiIsImlwIjoiMjIzLjEzOS4zNC4xMDgifQ.E0OHj3NJf2WRATdCCARefoyVTzQtRrXhoQkMaxerlic'
class Param():
    def __init__(self):
        self.url="https://api.finmindtrade.com/api/v4/data"
        self.dm=DateManage()
        self.start_date="2015-01-01"
        self.today=self.dm.transToString(self.dm.todayDate())
    def getData(self,parameter):
        resp=requests.get(self.url,params=parameter)
        try:
            data=resp.json()
            data=pd.DataFrame(data['data'])
            return data
        except:
            print('request error')   
class BasicTrans():
    def getPivotTable(self,table,values,columns='stock_id',index='date'):
        return table.pivot_table(index=index,values=values,columns=columns)
    def cleanSeason(self,year):
        if re.search('年',year):
            pos=re.search('年',year).start()
            return year[:pos]
        else:
            return year   
    def periodSum(self,n,pivotTable):
        return pivotTable.rolling(n).sum()
    def periodMean(self,n,pivotTable):
        return pivotTable.rolling(n).mean()
    def nShift(self,n,pivotTable):
        return pivotTable.shift(n,axis=0)
    def periodIncrease(self,n,pivotTable,m=1):
        periodMean=self.periodMean(m,pivotTable)
        return round((periodMean/self.nShift(n,periodMean)-1)*100)
    def deviationRate(self,pivotTable,meanTable,dec=0):
        return ((pivotTable/meanTable-1)*100).round(dec)

class FromAPI(Param):
    def __init__(self):
        super().__init__()
    def multiStock(self,start_date,dataset):
        parameter = {
            "dataset": dataset,
            "start_date": start_date,
            "token": token, # 參考登入，獲取金鑰
        }
        try:
            getData=self.getData(parameter)
            print("get multi data: ",start_date,dataset)
            return getData
        except:
            print("multi data does not get: ",start_date,dataset)
    def singleStock(self,data_id,start_date,end_date,dataset):
        parameter = {
            "dataset": dataset,
            "data_id": data_id,
            "start_date": start_date,
            "end_date":end_date,
            "token": token, # 參考登入，獲取金鑰
        }
        try:
            print('start get data',dataset)
            getData=self.getData(parameter)
            print("get single data: ",data_id,start_date,end_date,dataset)
            return getData
        except:
            print("single data does not get: ",data_id,start_date,end_date,dataset)        