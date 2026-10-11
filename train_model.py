
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load our example dataset
data = pd.read_csv("urls.csv")

# Separate URLs and their labels
X = data["url"]
y = data["label"]

# Convert URL text into numerical features
vectorizer = CountVectorizer(
    analyzer="char",
    ngram_range=(2, 5)
)

X_features = vectorizer.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_features,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)

print("Model training completed!")
print("Test accuracy:", accuracy_score(y_test, predictions))
print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))

# Save the model and vectorizer
with open("phishguard_model.pkl", "wb") as file:
    pickle.dump((vectorizer, model), file)

print("\nSaved model to phishguard_model.pkl")
