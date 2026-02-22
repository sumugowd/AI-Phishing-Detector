from flask import Flask, render_template, request
import joblib
import re
import nltk
from nltk.corpus import stopwords
from spellchecker import SpellChecker

# Download once (better to download manually in production)
nltk.download('stopwords')

app = Flask(__name__)

# Load model
model = joblib.load("model/model.pkl")

# Initialize tools
spell = SpellChecker()
stop_words = set(stopwords.words('english'))

# Store prediction history (temporary memory storage)
prediction_history = []

urgent_keywords_list = [
    "urgent", "verify", "immediately", "account",
    "bank", "click", "password", "login", "alert",
    "confirm", "security", "suspend", "limited",
    "action", "required", "update", "payment",
    "blocked", "warning", "rs", "bill", "claim",
    "reward", "offer", "won", "hurry", "save",
    "top-up", "pay", "prize", "bonus", "cash",
    "jackpot", "free", "extra"
]


def extract_features(email_text):
    words = email_text.split()

    num_words = len(words)
    num_unique_words = len(set(words))
    num_stopwords = len([w for w in words if w.lower() in stop_words])

    links = re.findall(r"https?://\S+|www\.\S+", email_text)
    num_links = len(links)

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

    emails = re.findall(r"\S+@\S+", email_text)
    num_email_addresses = len(emails)

    misspelled = spell.unknown(words)
    num_spelling_errors = len(misspelled)

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

    # Initialize variables for both GET and POST
    result = None
    confidence = None
    risk_level = None
    features = None   # 🔥 important fix

    if request.method == "POST":

        email_text = request.form.get("email_text", "").strip()

        if email_text == "":
            return render_template(
                "dashboard.html",
                result="⚠️ Please enter email content",
                confidence=0,
                risk_level="N/A",
                features=None,
                history=prediction_history
            )

        features = extract_features(email_text)

        # Base ML probability
        prob = model.predict_proba([features])[0][1]

        num_links = features[3]
        num_urgent_keywords = features[7]

        # Hybrid heuristic boosting
        if "bit.ly" in email_text or "tinyurl" in email_text or "t.co" in email_text:
            prob += 0.20

        prob += 0.08 * num_links
        prob += 0.05 * num_urgent_keywords

        if num_links > 0 and num_urgent_keywords > 0:
            prob += 0.10

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

        # Save in memory history
        prediction_history.append({
            "text": email_text[:60] + "...",
            "result": result,
            "confidence": confidence,
            "risk": risk_level
        })

        # Keep only last 10 records (professional touch)
        if len(prediction_history) > 10:
            prediction_history.pop(0)

    return render_template(
        "dashboard.html",
        result=result,
        confidence=confidence,
        risk_level=risk_level,
        features=features,
        history=prediction_history
    )


if __name__ == "__main__":
    app.run(debug=True)