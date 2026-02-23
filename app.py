from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- PREDICT ROUTE ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        product_name = data.get("product", "")
        review_text = data.get("review", "")

        # Load model only when needed (prevents Render freezing)
        model = pickle.load(open("fake_review_model.pkl", "rb"))
        vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

        # Transform and predict
        transformed_text = vectorizer.transform([review_text])
        prediction = model.predict(transformed_text)

        return jsonify({
            "product": product_name,
            "prediction": str(prediction[0])
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)