from flask import Flask,redirect,url_for,render_template
from data import *
import json

app = Flask(__name__)

firstNav='price'
singleDataNav = ['price', 'month revenue','statement sheet','dividend','overview']
cache={}

@app.route("/")
def home():
    return render_template("index.html", firstNav=firstNav,navData=singleDataNav)

@app.route("/table/<stockId>")
def table(stockId):
    data=BasicTable(stockId)
    cache['stockId']=stockId
    # cache['priceTable']=data.priceTable
    # cache['revenueTable']=data.revenueTable
    # cache['financialTaable']=data.financialTable
    cache['dayDates']=data.dayDates
    cache['monthDates']=data.monthDates
    cache['seasonDates']=data.seasonDates
    allContent=data.allContent()
    return json.dumps(allContent)
@app.route("/overview")
def overview():
    print('get overview')
    # print(cache['stockId'])

    return cache['stockId']

if __name__ == "__main__":
    app.run(debug=True)