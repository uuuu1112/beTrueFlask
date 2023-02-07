import requests
# import copy
import pandas as pd
from dateManage import *

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
class FromAPI(Param):
    def __init__(self):
        super().__init__()
    def multiStock(self,start_date,dataset):
        parameter = {
            "dataset": dataset,
            "start_date": start_date,
            "token": "", # 參考登入，獲取金鑰
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
            "token": "", # 參考登入，獲取金鑰
        }
        try:
            print('start get data',dataset)
            getData=self.getData(parameter)
            print("get single data: ",data_id,start_date,end_date,dataset)
            return getData
        except:
            print("single data does not get: ",data_id,start_date,end_date,dataset)        