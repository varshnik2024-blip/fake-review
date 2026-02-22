import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1️⃣ Load dataset
df = pd.read_csv("fake reviews dataset.csv")

# 2️⃣ Encode labels
# We will map 'CG' -> 1 (fake) and 'OR' -> 0 (real)
df["label_encoded"] = df["label"].map({"CG": 1, "OR": 0})

# 3️⃣ Define the features and target
X = df["text_"]        # Use the correct text column name
y = df["label_encoded"]

# 4️⃣ Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5️⃣ Vectorize text with TF-IDF
tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_tfidf = tfidf.fit_transform(X_train)

# 6️⃣ Train a classifier (Logistic Regression)
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_tfidf, y_train)

# 7️⃣ Save the model and vectorizer
pickle.dump(clf, open("fake_review_model.pkl", "wb"))
pickle.dump(tfidf, open("tfidf_vectorizer.pkl", "wb"))

print("✅ Model training completed and saved!")