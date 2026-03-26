from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# 🔴 PASTE YOUR API KEY HERE
import os
API_KEY = os.environ.get("API_KEY")


def get_products(query):
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "amazon",
        "k": query,
        "amazon_domain": "amazon.in",
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("FULL RESPONSE:", data)  # 🔍 DEBUG

    products = []

    # ✅ HANDLE BOTH POSSIBLE KEYS
    results = data.get("shopping_results") or data.get("organic_results") or []

    for item in results[:6]:
        title = item.get("title", "No Title")

        # 🔥 IMAGE FIX (IMPORTANT)
        image = (
            item.get("thumbnail")
            or item.get("image")
            or item.get("thumbnail_url")
            or "https://via.placeholder.com/300?text=No+Image"
        )

        link = item.get("link", "#")

        price = item.get("price") or item.get("extracted_price") or "N/A"

        fake = random.randint(10, 30)
        real = 100 - fake

        products.append({
            "title": title,
            "image": image,
            "link": link,
            "price": price,
            "fake": fake,
            "real": real
        })

    print("FINAL PRODUCTS:", products)  # 🔍 DEBUG

    return products


@app.route("/", methods=["GET", "POST"])
def home():
    products = []
    query = ""

    if request.method == "POST":
        query = request.form.get("product")

        if query:
            products = get_products(query)

    return render_template("index.html", products=products, query=query)


if __name__ == "__main__":
    app.run(debug=True)