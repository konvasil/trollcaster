import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB

# Extended dataset with more troll and non-troll examples
X = [
    "hello how are you",
    "this is spam",
    "you are a troll",
    "have a nice day",
    "buy cheap stuff now",
    "hack this site",
    "nice to meet you",
    "I love this!",
    "you suck",
    "go away loser",
    "stupid idiot",
    "I hope you die",
    "cheap pills online",
    "amazing work!",
    "visit my site for free stuff",
    "you're trash",
    "this sucks",
    "great job everyone",
    "get rekt kid",
    "what a dumb post",
    "this is pathetic"
]
y = [
    0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1,
    1, 0, 1, 1, 1, 0, 1, 1, 1
]  # 1 = troll, 0 = normal

# Train a simple model
model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(X, y)

# Save model to ml/model.pkl
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to ml/model.pkl")
