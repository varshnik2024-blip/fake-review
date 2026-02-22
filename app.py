from flask import Flask, request, jsonify, render_template
import pickle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

# Load the trained model and the vectorizer
model = pickle.load(open("fake_review_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    product_name = data.get("product", "")
    review_text = data.get("review", "")

    # ===== VADER Sentiment Analysis =====
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(review_text)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # ===== Fake/Real Prediction =====
    vect = vectorizer.transform([review_text])
    prob_fake = model.predict_proba(vect)[0][1]

    percent_fake = round(prob_fake * 100, 2)
    percent_real = round((1 - prob_fake) * 100, 2)

    if prob_fake >= 0.5:
        result_text = f"{percent_fake}% Fake, {percent_real}% Real"
    else:
        result_text = f"{percent_real}% Real, {percent_fake}% Fake"

    return jsonify({
        "product": product_name,
        "prediction": result_text,
        "sentiment": sentiment
    })


if __name__ == "__main__":
    app.run(debug=True)