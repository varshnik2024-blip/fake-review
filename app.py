from flask import Flask, render_template, request, redirect, url_for
import requests
import random
import os

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

# 🔐 SIMPLE USER STORAGE (for login)
users = {}


def get_products(query):
    url = "https://serpapi.com/search.json"

    products = []
    seen_links = set()

    for start in [0, 20, 40]:

        params = {
            "engine": "amazon",
            "k": query,
            "amazon_domain": "amazon.in",
            "api_key": API_KEY,
            "num": 20,
            "start": start
        }

        response = requests.get(url, params=params)
        data = response.json()

        results = data.get("shopping_results") or data.get("organic_results") or []

        for item in results:
            link = item.get("link")

            if not link or link in seen_links:
                continue

            seen_links.add(link)

            title = item.get("title", "No Title")

            image = (
                item.get("thumbnail")
                or item.get("image")
                or item.get("thumbnail_url")
                or "https://via.placeholder.com/300?text=No+Image"
            )

            price = item.get("price") or item.get("extracted_price") or "N/A"

            rating = item.get("rating") or 0

            fake = random.randint(10, 30)
            real = 100 - fake

            products.append({
                "title": title,
                "image": image,
                "link": link,
                "price": price,
                "rating": rating,
                "fake": fake,
                "real": real
            })

    products = sorted(products, key=lambda x: x["rating"], reverse=True)

    return products[:50]


# 🔐 LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")


# 🔐 SIGNUP
@app.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    password = request.form.get("password")

    users[email] = password
    return redirect(url_for("website"))


# 🔐 LOGIN CHECK
@app.route("/login", methods=["POST"])
def login_user():
    email = request.form.get("email")
    password = request.form.get("password")

    if email in users and users[email] == password:
        return redirect(url_for("website"))
    else:
        return "Invalid Login ❌"


# 🌐 YOUR ORIGINAL WEBSITE (UNCHANGED)
@app.route("/home", methods=["GET", "POST"])
def website():
    products = []
    query = ""

    if request.method == "POST":
        query = request.form.get("product")

        if query:
            products = get_products(query)

    return render_template("index.html", products=products, query=query)


if __name__ == "__main__":
    app.run(debug=True)