import datetime

class DateManage():
    # 今天的日期
    def todayDate(self):
        return datetime.date.today()
    # 轉化成日期
    def transToDate(self,dateString):
        return datetime.datetime.strptime(dateString,'%Y-%m-%d')
    # get time stamp
    def getTimeStamp(self,dateString):
        date=self.transToDate(dateString)
        return datetime.datetime.timestamp(date)
    # 日期轉為文字    
    def transToString(self,date):
        return date.strftime('%Y-%m-%d')
    def seasonRelease(self,dateStr):
        date=self.transToDate(dateStr)
        if date.month==3:
            return str(date.year)+"-05-15"
        elif date.month==6:
            return str(date.year)+"-08-14"
        elif date.month==9:
            return str(date.year)+"-11-14"
        else:
            return str(date.year-1)+"-03-31"  
    def seasonTrans(self,dateList):
        transDate=dateList
        for i in range(len(transDate)):
            transDate[i]=self.seasonRelease(dateList[i])
        return transDate
    def monthRelease(self,dateStr):
        date=self.transToDate(dateStr)
        if date.month==1:
            return str(date.year-1)+"-12-10"
        else:
            if len(str(date.month-1))==1:
                return str(date.year)+"-0"+str(date.month-1)+"-10"
            else:
                return str(date.year)+"-"+str(date.month-1)+"-10" 
    def monthTrans(self,dateList):
        transDate=dateList
        for i in range(len(transDate)):
            transDate[i]=self.monthRelease(dateList[i])
        return transDate          