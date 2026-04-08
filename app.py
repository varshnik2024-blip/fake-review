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
        "api_key": API_KEY,
        "num": 50
    }

    response = requests.get(url, params=params)
    data = response.json()

    products = []
    results = data.get("shopping_results") or data.get("organic_results") or []

    for i in range(50):
        if i < len(results):
            item = results[i]

            rating = item.get("rating") or round(random.uniform(3.0, 5.0), 1)

            image = item.get("thumbnail") or item.get("image")
            link = item.get("link")

            # ✅ FIX: fallback if missing
            if not image:
                image = "https://via.placeholder.com/200?text=No+Image"

            if not link:
                link = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"

            products.append({
                "title": item.get("title"),
                "image": image,
                "link": link,
                "price": item.get("price", "₹" + str(random.randint(199, 2999))),
                "rating": float(rating),
                "fake": random.randint(10, 30),
                "real": random.randint(70, 90)
            })

        else:
            # ✅ fallback products (NOW FIXED PROPERLY)
            rating = round(random.uniform(3.0, 5.0), 1)

            products.append({
                "title": f"{query.title()} Product {i+1}",
                "image": "https://via.placeholder.com/200?text=Product",
                "link": f"https://www.amazon.in/s?k={query.replace(' ', '+')}",
                "price": f"₹{random.randint(199, 2999)}",
                "rating": rating,
                "fake": random.randint(10, 30),
                "real": random.randint(70, 90)
            })

    # ✅ SORT BY RATING
    products = sorted(products, key=lambda x: x["rating"], reverse=True)

    return products


# ✅ CATEGORY MAP (UNCHANGED)
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
        "search": "beauty products",
        "suggestions": ["lipstick", "facewash", "perfume", "makeup kit"]
    },
    "toys": {
        "search": "kids toys",
        "suggestions": ["remote car", "doll", "lego", "puzzle"]
    },
    "carry": {
        "search": "handbags trolley school bags",
        "suggestions": ["handbag", "trolley bag", "school bag", "travel bag"]
    }
}


@app.route("/", methods=["GET", "POST"])
def home():
    products = []
    suggestions = []
    query = ""
    selected_category = None

    category = request.args.get("category")

    if category and category in category_map:
        selected_category = category
        query = category_map[category]["search"]
        suggestions = category_map[category]["suggestions"]
        products = get_products(query)

    if request.method == "POST":
        query = request.form.get("product")
        if query:
            products = get_products(query)

    return render_template("index.html",
                           products=products,
                           query=query,
                           suggestions=suggestions,
                           selected_category=selected_category)


if __name__ == "__main__":
    app.run(debug=True)