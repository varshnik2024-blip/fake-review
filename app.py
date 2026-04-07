from flask import Flask, render_template, request
import requests
import random
import os

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")


# 🔹 Fetch products
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

    products = []
    results = data.get("shopping_results") or data.get("organic_results") or []

    for item in results[:6]:
        products.append({
            "title": item.get("title", "No Title"),
            "image": item.get("thumbnail") or item.get("image") or "https://via.placeholder.com/300",
            "link": item.get("link", "#"),
            "price": item.get("price", "N/A"),
            "fake": random.randint(10, 30),
            "real": random.randint(70, 90)
        })

    return products


# 🔥 CATEGORY SUGGESTIONS
category_suggestions = {
    "electronics": "earbuds, headphones, smart watch",
    "textiles": "kurti, saree, dresses",
    "books": "best books, novels",
    "home": "kitchen appliances, furniture",
    "beauty": "makeup kit, skincare"
}


@app.route("/", methods=["GET", "POST"])
def home():
    products = []
    query = ""
    selected_category = ""

    # 🔹 Category clicked → show suggestions
    category = request.args.get("category")
    if category:
        selected_category = category
        query = category_suggestions.get(category, category)
        products = get_products(query)

    # 🔹 User search (inside category or normal)
    if request.method == "POST":
        user_query = request.form.get("product")
        if user_query:
            if selected_category:
                query = selected_category + " " + user_query
            else:
                query = user_query

            products = get_products(query)

    return render_template(
        "index.html",
        products=products,
        query=query,
        selected_category=selected_category
    )


if __name__ == "__main__":
    app.run(debug=True)