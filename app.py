from flask import Flask, render_template, request
import requests
import random
import os

app = Flask(__name__)

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

    products = []
    results = data.get("shopping_results") or data.get("organic_results") or []

    for item in results[:8]:
        products.append({
            "title": item.get("title"),
            "image": item.get("thumbnail") or item.get("image"),
            "link": item.get("link"),
            "price": item.get("price", "N/A"),
            "fake": random.randint(10, 30),
            "real": random.randint(70, 90)
        })

    return products


# 🔥 CATEGORY MAP
category_map = {
    "electronics": {
        "search": "electronics gadgets",
        "suggestions": ["earbuds", "smartphone", "laptop", "smartwatch"]
    },
    "home": {
        "search": "home kitchen appliances",
        "suggestions": ["mixer", "fan", "sofa", "lamp"]
    },
    "jewellery": {
        "search": "jewellery",
        "suggestions": ["necklace", "earrings", "ring", "bracelet"]
    },
    "men": {
        "search": "men clothing",
        "suggestions": ["shirt", "jeans", "jacket", "tshirt"]
    },
    "women": {
        "search": "women clothing",
        "suggestions": ["kurti", "saree", "dress", "top"]
    },
    "kids": {
        "search": "kids clothing",
        "suggestions": ["kids dress", "baby frock", "school uniform", "kids shoes"]
    },
    "cosmetics": {
        "search": "cosmetics beauty products",
        "suggestions": ["lipstick", "facewash", "perfume", "makeup kit"]
    },
    "toys": {
        "search": "kids toys",
        "suggestions": ["remote car", "doll", "lego", "puzzle"]
    }
}


@app.route("/", methods=["GET", "POST"])
def home():
    products = []
    suggestions = []
    query = ""

    category = request.args.get("category")
    query_from_url = request.args.get("query")

    # CATEGORY CLICK
    if category and category in category_map:
        query = category_map[category]["search"]
        suggestions = category_map[category]["suggestions"]
        products = get_products(query)

    # SUGGESTION CLICK
    if query_from_url:
        query = query_from_url
        products = get_products(query)

    # SEARCH BAR
    if request.method == "POST":
        query = request.form.get("product")
        if query:
            products = get_products(query)

    return render_template("index.html",
                           products=products,
                           query=query,
                           suggestions=suggestions)


if __name__ == "__main__":
    app.run(debug=True)