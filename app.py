from flask import Flask, render_template, request
import joblib
import re
import nltk
from nltk.corpus import stopwords
from spellchecker import SpellChecker

# Download stopwords once
nltk.download('stopwords')

# Initialize Flask
app = Flask(__name__)

# Load trained model
model = joblib.load("model/model.pkl")

# Initialize spell checker
spell = SpellChecker()

# Stopwords
stop_words = set(stopwords.words('english'))

# Urgent / suspicious keywords (Email + SMS focused)
urgent_keywords_list = [
    "urgent", "verify", "immediately", "account",
    "bank", "click", "password", "login", "alert",
    "confirm", "security", "suspend", "limited",
    "action", "required", "update", "payment",
    "blocked", "warning", "rs", "bill", "claim",
    "reward", "offer", "won", "hurry", "save",
    "top-up", "pay", "prize","bonus", "cash", 
    "jackpot", "top-up", "free", "extra"
]


def extract_features(email_text):
    words = email_text.split()

    num_words = len(words)
    num_unique_words = len(set(words))
    num_stopwords = len([w for w in words if w.lower() in stop_words])

    # 🔹 Detect links (http, https, www)
    links = re.findall(r"https?://\S+|www\.\S+", email_text)
    num_links = len(links)

    # 🔹 Extract domains safely
    domains = set()
    for link in links:
        try:
            if "://" in link:
                domain = link.split("/")[2]
            else:
                domain = link.split("/")[0]
            domains.add(domain)
        except:
            pass

    num_unique_domains = len(domains)

    # 🔹 Detect email addresses
    emails = re.findall(r"\S+@\S+", email_text)
    num_email_addresses = len(emails)

    # 🔹 Spelling errors
    misspelled = spell.unknown(words)
    num_spelling_errors = len(misspelled)

    # 🔹 Count urgent keywords
    num_urgent_keywords = sum(
        1 for w in words if w.lower().strip(".,!:") in urgent_keywords_list
    )

    return [
        num_words,
        num_unique_words,
        num_stopwords,
        num_links,
        num_unique_domains,
        num_email_addresses,
        num_spelling_errors,
        num_urgent_keywords
    ]


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    confidence = None
    risk_level = None

    if request.method == "POST":
        email_text = request.form["email_text"]

        features = extract_features(email_text)

        # 🔹 Base ML probability
        prob = model.predict_proba([features])[0][1]

        # 🔹 Hybrid Heuristic Boost
        num_links = features[3]
        num_urgent_keywords = features[7]

        # Strong boost for shortened URLs
        if "bit.ly" in email_text or "tinyurl" in email_text or "t.co" in email_text:
             prob += 0.20


        # Link weight
        prob += 0.08 * num_links

        # Urgent keyword weight
        prob += 0.05 * num_urgent_keywords

        # SMS style phishing pattern boost
        if num_links > 0 and num_urgent_keywords > 0:
            prob += 0.10

        # Cap probability to 1
        prob = min(prob, 1.0)

        threshold = 0.20

        if prob > threshold:
            result = "⚠️ Phishing Email Detected"
        else:
            result = "✅ Safe Email"

        confidence = round(prob * 100, 2)

        if prob < 0.20:
            risk_level = "Low Risk"
        elif prob < 0.50:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        risk_level=risk_level
    )


if __name__ == "__main__":
    app.run(debug=True)
