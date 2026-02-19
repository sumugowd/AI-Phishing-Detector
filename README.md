# 🛡️ AI-Based Phishing & Smishing Detection System

This project is a hybrid Machine Learning system that detects phishing emails and SMS (smishing) messages using:

- Random Forest Classifier
- Automated Feature Engineering
- Heuristic Risk Boosting
- Probability Threshold Tuning
- Flask Web Interface

The system classifies text messages as:

- ✅ Safe Email
- ⚠️ Phishing Email Detected

It also provides:
- Confidence Score (%)
- Risk Level (Low / Medium / High)

---

## 🚀 Project Highlights

- Trained on 524k+ phishing samples
- Handles class imbalance
- Detects shortened URLs (bit.ly, tinyurl, etc.)
- Detects urgency & financial keywords
- Spell-check based anomaly detection
- Hybrid ML + rule-based enhancement
- Real-time web interface using Flask

---

## 🧠 How It Works

1. User pastes email/SMS content.
2. The system extracts features:
   - Number of words
   - Unique words
   - Stopwords count
   - Number of links
   - Unique domains
   - Email addresses
   - Spelling errors
   - Urgent keywords
3. Random Forest predicts phishing probability.
4. Heuristic boosting adjusts probability.
5. Final classification and risk level are displayed.

---

## 📁 Dataset

This project uses the following public dataset:

🔗 Email Phishing Dataset (Kaggle)  
https://www.kaggle.com/datasets/ethancratchley/email-phishing-dataset/data

⚠️ Important:
Due to Kaggle dataset licensing terms, the dataset is NOT included in this repository.

Please download the dataset manually from Kaggle and place it inside the `data/` folder before training.

Example:

```
AI-Phishing-Detector/
├── data/
│   └── phishing.csv
```

---

## 🏗️ Project Structure

```
AI-Phishing-Detector/
│
├── app.py
├── train.py
├── requirements.txt
├── templates/
│   └── index.html
├── data/
│   └── (Place Kaggle dataset here)
├── model/
│   └── (Generated after training)
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/sumugowd/AI-Phishing-Detector.git
cd AI-Phishing-Detector
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Download Dataset

Download from:
https://www.kaggle.com/datasets/ethancratchley/email-phishing-dataset/data

Place the CSV file inside:

```
data/
```

### 5️⃣ Train the Model

```bash
python train.py
```

This generates:

```
model/model.pkl
```

### 6️⃣ Run the Web App

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

## 📊 Model Details

- Algorithm: Random Forest Classifier
- Handles class imbalance using weighted classes
- Custom probability threshold tuning
- Hybrid risk boosting for:
  - Shortened URLs
  - Financial keywords
  - Urgent messages

---

## 🧪 Example Test Cases

### 🔴 Phishing Example
```
URGENT! Verify your bank account immediately.
Click here: http://secure-update-bankinfo.com
```

### 🟢 Safe Example
```
Hi Team,
Reminder: Meeting scheduled for tomorrow at 4 PM.
```

---

## ⚠️ Limitations

- Model performance depends on training data similarity.
- New phishing patterns may require retraining.
- Dataset not included due to licensing policies.

---

## 🛠️ Technologies Used

- Python
- Scikit-learn
- Flask
- Pandas
- NLTK
- Regex
- PySpellChecker

---

## 🎓 Developed For

Center of Excellence (COE) Academic Project

---

## 👨‍💻 Author

Sumanth G