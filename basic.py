import requests
import copy
import pandas as pd
from dateManage import *

class Param():
    def __init__(self):
        self.url="https://api.finmindtrade.com/api/v4/data"
        self.parameter={}
        self.parameter2=copy.copy(self.parameter)  
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
        self.parameter['start_date']=start_date
        self.parameter['dataset']=dataset
        try:
            getData=self.getData(self.parameter)
            print("get multi data: ",start_date,dataset)
            return getData
        except:
            print("multi data does not get: ",start_date,dataset)
    def singleStock(self,data_id,start_date,end_date,dataset):
        self.parameter2['data_id']=data_id
        self.parameter2['start_date']=start_date
        self.parameter2['end_date']=end_date
        self.parameter2['dataset']=dataset
        try:
            getData=self.getData(self.parameter2)
            print("get single data: ",data_id,start_date,end_date,dataset)
            return getData
        except:
            print("single data does not get: ",data_id,start_date,end_date,dataset)        