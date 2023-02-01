from flask import Flask,redirect,url_for,render_template

app = Flask(__name__)

firstNav='price'
singleDataNav = ['price', 'month revenue','statement sheet','dividend','overview']
cache={}

@app.route("/")
def home():
    return render_template("index.html", firstNav=firstNav,navData=singleDataNav)
@app.route("/<stockId>")
def stockId(stockId):
    return f"stock id {stockId}"


if __name__ == "__main__":
    app.run(debug=True)