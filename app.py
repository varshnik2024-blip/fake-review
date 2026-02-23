from flask import Flask, request, jsonify, render_template
import pickle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

# Load model and vectorizer
model = pickle.load(open("fake_review_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        product_name = data.get("product", "")
        review_text = data.get("review", "")

        # Transform text
        transformed_text = vectorizer.transform([review_text])

        # Prediction
        prediction = model.predict(transformed_text)
        probability = model.predict_proba(transformed_text)

        confidence = float(max(probability[0])) * 100

        # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        sentiment_score = analyzer.polarity_scores(review_text)

        if sentiment_score['compound'] >= 0.05:
            sentiment = "Positive"
        elif sentiment_score['compound'] <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return jsonify({
            "product": product_name,
            "prediction": str(prediction[0]),
            "confidence": round(confidence, 2),
            "sentiment": sentiment
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)