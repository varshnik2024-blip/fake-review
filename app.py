from flask import Flask, render_template, request
import requests
import random
import os

app = Flask(__name__)

# 🔐 GET API KEY FROM ENV
API_KEY = os.environ.get("API_KEY")


def get_products(query):
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "amazon",
        "k": query,
        "amazon_domain": "amazon.in",
        "api_key": API_KEY,
        "num": 20   # 🔥 GET UP TO 20 PRODUCTS
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("FULL RESPONSE:", data)  # DEBUG

    products = []

    # HANDLE DIFFERENT POSSIBLE KEYS
    results = data.get("shopping_results") or data.get("organic_results") or []

    # 🔥 SHOW UP TO 20 PRODUCTS
    for item in results[:20]:
        title = item.get("title", "No Title")

        image = (
            item.get("thumbnail")
            or item.get("image")
            or item.get("thumbnail_url")
            or "https://via.placeholder.com/300?text=No+Image"
        )

        link = item.get("link", "#")

        price = item.get("price") or item.get("extracted_price") or "N/A"

        # RANDOM FAKE/REAL (for demo)
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

    print("FINAL PRODUCTS:", products)  # DEBUG

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


# 🔥 IMPORTANT FOR RENDER DEPLOYMENT
if __name__ == "__main__":
    app.run(debug=True)