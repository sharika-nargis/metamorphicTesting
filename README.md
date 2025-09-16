# Metamorphic Testing Automation for Sentiment Analysis ML Model  

This project demonstrates **Metamorphic Testing** automation using **Selenium** and **NLTK WordNet** on a publicly available sentiment analysis tool.  
It automatically verifies that the model’s sentiment predictions remain consistent under **metamorphic transformations** (like synonym replacements).

---

## 🚀 Features  
- Automates text input and prediction extraction from [ClientZen Sentiment Analysis Tool](https://www.clientzen.io/sentiment-analysis-tool).  
- Implements **Metamorphic Relations (MRs)** to test ML model robustness:
  - **Synonym replacement**: replacing words with synonyms should not change the sentiment prediction.
  - Can be extended to other MRs (negation, scaling, etc.).
- Collects and compares model predictions between original and transformed inputs.
- Generates pass/fail output for each MR automatically.

---

## 🛠️ Tech Stack  
- **Python 3.10+**
- **Selenium WebDriver** (Chrome)
- **webdriver-manager**
- **NLTK WordNet**

---

## 📂 Project Structure  
project-root/
│
├── metamorphic_test.py # Main script
├── requirements.txt # Dependencies
└── README.md # This file


---

## Installation  

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/metamorphic-sentiment-testing.git
   cd metamorphic-sentiment-testing

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Download NLTK WordNet data (first run only):
   ```bash
   import nltk
   nltk.download("wordnet")
   nltk.download("omw-1.4")

## 📝 Usage
1. Run the main test script:
   ```bash
   python metamorphic_test.py

2. The script will:
- Open the ClientZen sentiment analysis page.
- Input the original text (e.g. “I love this movie”).
- Transform the text using WordNet synonyms.
- Compare the predictions of the original and transformed text.
- Print results to the console:
   ```text
   Original: I love this movie → Positive
   Transformed: I enjoy this movie → Positive
   MR Satisfied

## 🧠 How It Works
Metamorphic Testing:
Traditional testing requires labeled ground truth data. Metamorphic Testing instead defines relations that must hold true even if the input changes in certain predictable ways.
Example MR: If we replace a word with its synonym, the overall sentiment should not change.

Synonym Replacement:
We use NLTK WordNet to find synonyms for words in the input text.
The transformed text is then re-submitted to the model, and predictions are compared.

## 📈 Possible Extensions
- Add more MRs:
  > Negation (I like → I do not dislike).
  > Input scaling (repeating words).
  > Word order variations.
- Generate HTML/CSV reports of test runs.
- Integrate with CI/CD pipeline (GitHub Actions).

## ⚠️ Disclaimer
This project is for educational and testing purposes only. It uses a public sentiment analysis demo site (ClientZen) to illustrate testing concepts.

## 🧑‍💻 Author
Sharika Nargis — Software Quality Assurance Engineer
