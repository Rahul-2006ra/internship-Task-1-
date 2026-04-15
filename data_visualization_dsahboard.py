# ==========================================
# API Integration + Data Visualization Project
# ==========================================
# This script fetches cryptocurrency price data from a public API
# and creates a visualization dashboard using Flask + Matplotlib

import requests
import matplotlib.pyplot as plt
from flask import Flask, render_template_string

app = Flask(__name__)

# ------------------------------------------
# Step 1: Fetch data from API
# ------------------------------------------
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "7"
    }
    response = requests.get(url, params=params)
    data = response.json()

    prices = data["prices"]

    # Extract time and price
    times = [i[0] for i in prices]
    values = [i[1] for i in prices]

    return times, values

# ------------------------------------------
# Step 2: Create visualization
# ------------------------------------------
def create_plot(times, values):
    plt.figure()
    plt.plot(values)
    plt.title("Bitcoin Price - Last 7 Days")
    plt.xlabel("Time Index")
    plt.ylabel("Price (USD)")

    file_path = "static/plot.png"
    plt.savefig(file_path)
    plt.close()

    return file_path

# ------------------------------------------
# Step 3: Flask Dashboard
# ------------------------------------------
@app.route('/')
def dashboard():
    times, values = fetch_crypto_data()
    plot_path = create_plot(times, values)

    html = f"""
    <html>
    <head>
        <title>Crypto Dashboard</title>
    </head>
    <body style='text-align:center; font-family:Arial;'>
        <h1>📊 Bitcoin Price Dashboard</h1>
        <img src='/{plot_path}' width='700'>
        <p>Data fetched from CoinGecko API</p>
    </body>
    </html>
    """

    return render_template_string(html)

# ------------------------------------------
# Step 4: Run server
# ------------------------------------------
if __name__ == '__main__':
    import os
    if not os.path.exists("static"):
        os.makedirs("static")

    app.run(debug=True)
