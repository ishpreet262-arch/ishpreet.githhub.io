from flask import Flask, render_template, request
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# create static folder
if not os.path.exists("static"):
    os.makedirs("static")

# -------- LOGIN PAGE --------
@app.route('/')
def login():
    return render_template("login.html")

# -------- LOGIN CHECK --------
@app.route('/home', methods=['POST'])
def home():
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "1234":
        return render_template("index.html")
    else:
        return "<h3>Login Failed</h3>"

# -------- PREDICT FUNCTION --------
@app.route('/predict', methods=['POST'])
def predict():
    stock = request.form['stock'].strip().upper()

    try:
        us_stocks = ["AAPL","TSLA","MSFT","GOOG","AMZN","META","NVDA"]
        index_symbols = ["^NSEI","^NSEBANK","^DJI","^IXIC","^BSESN"]
        crypto_symbols = ["BTC-USD","ETH-USD","DOGE-USD","SOL-USD","BNB-USD"]

        # symbol handling
        if stock in index_symbols or stock in crypto_symbols:
            pass
        elif stock not in us_stocks and ".NS" not in stock:
            stock = stock + ".NS"

        ticker = yf.Ticker(stock)
        df = ticker.history(period="3mo")

        if df.empty:
            return "<h3>Data not loading. Try AAPL or BTC-USD</h3>"

        last_price = float(df['Close'].iloc[-1])
        avg_price = float(df['Close'].mean())
        predicted_price = (last_price + avg_price)/2

        # graph
        plt.figure(figsize=(7,4))
        plt.plot(df['Close'])
        plt.title(stock + " Live Price")
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.tight_layout()
        plt.savefig("static/graph.png")
        plt.close()

        signal = "BUY 📈" if predicted_price > last_price else "SELL 📉"

        return render_template("result.html",
                               stock=stock,
                               price=round(last_price,2),
                               prediction=round(predicted_price,2),
                               signal=signal)

    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"

# -------- RUN SERVER --------
if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
