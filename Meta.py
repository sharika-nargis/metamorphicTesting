"""
Metamorphic Testing Automation for ML Model (Sentiment Analysis Web App)
"""
from __future__ import annotations
import re, time, nltk
from typing import Iterable, Tuple
from nltk.corpus import stopwords, wordnet
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Download required NLTK data
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("averaged_perceptron_tagger", quiet=True)

stop_words: set[str] = set(stopwords.words("english"))

def start_driver(headless: bool = False) -> webdriver.Chrome:
    """Start Chrome with sensible defaults."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(40)
    return driver

# Ensure wordnet present
try:
    wordnet.synsets("test")
except LookupError:
    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)

RESULTS_URL: str = "https://www.clientzen.io/sentiment-analysis-tool-results"
TOOL_URL: str = "https://www.clientzen.io/sentiment-analysis-tool"

def find_first_present(
    screen: webdriver.Chrome,
    locators: Iterable[Tuple[By, str]],
    timeout: float = 8.0
) -> webdriver.remote.webelement.WebElement:
    """Return first displayed element matching any locator within timeout."""
    end = time.time() + timeout
    while time.time() < end:
        for by, sel in locators:
            try:
                el = screen.find_element(by, sel)
                if el.is_displayed():
                    return el
            except Exception:
                continue
        time.sleep(0.25)
    raise TimeoutError("No candidate element found for provided locators.")

def type_text_and_submit(driver: webdriver.Chrome, text: str) -> None:
    """Enter text in the tool input and submit for analysis."""
    driver.get(TOOL_URL)
    input_candidates: list[Tuple[By, str]] = [(By.CSS_SELECTOR, "#Happiness-Score-Text-3")]
    box = find_first_present(driver, input_candidates, timeout=10)
    try:
        tag = box.tag_name.lower()
    except Exception:
        tag = ""
    if tag in ("textarea", "input"):
        try:
            box.clear()
        except Exception:
            pass
    box.click()
    box.send_keys(text)
    driver.find_element(By.XPATH, "//input[@id='happiness-score-button']").click()

def wait_for_results_and_extract_sentiment(driver: webdriver.Chrome) -> str:
    """Wait for sentiment result and extract it."""
    WebDriverWait(driver, 20).until(EC.url_contains("/sentiment-analysis-tool-results"))
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(.,'Your text was analyzed') or contains(.,'Results')]")
        )
    )
    try:
        node = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h4[contains(text(), 'Positive') or contains(text(), 'Negative') or contains(text(), 'Neutral')]")
            )
        )
        haystack: str = (node.text or "") + " " + driver.page_source
    except Exception:
        haystack = driver.page_source
    m = re.search(r"\b(Positive|Negative|Neutral)\b", haystack, re.I)
    return m.group(1).capitalize() if m else "Unknown"

def get_prediction(driver: webdriver.Chrome, text: str) -> str:
    """Run full prediction flow on ClientZen."""
    type_text_and_submit(driver, text)
    return wait_for_results_and_extract_sentiment(driver)

def synonym_replacement(text: str) -> str:
    """Replace first non-stopword with a synonym if possible."""
    words: list[str] = text.split()
    pos_tags: list[Tuple[str, str]] = nltk.pos_tag(words)
    for i, (word, pos) in enumerate(pos_tags):
        if word.lower() in stop_words:
            continue
        wn_pos = None
        if pos.startswith("J"):
            wn_pos = wordnet.ADJ
        elif pos.startswith("V"):
            wn_pos = wordnet.VERB
        elif pos.startswith("N"):
            wn_pos = wordnet.NOUN
        elif pos.startswith("R"):
            wn_pos = wordnet.ADV
        if wn_pos:
            syns = wordnet.synsets(word, pos=wn_pos)
            for syn in syns:
                if syn:
                    hi = [l for l in syn.lemmas()]
                    same = [lemma for lemma in hi if lemma.name() == word.lower()]
                    alternatives = [lemma.name() for lemma in hi if lemma.name() != word.lower()]
                    if alternatives:
                        words[i] = alternatives[0]
                        return " ".join(words)
    return text

if __name__ == "__main__":
    driver = start_driver(headless=False)
    try:
        original_text: str = "I love movie"
        original_pred: str = get_prediction(driver, original_text)
        transformed_text: str = synonym_replacement(original_text)
        transformed_pred: str = get_prediction(driver, transformed_text)
        print(f"Original:    {original_text}  → {original_pred}")
        print(f"Transformed: {transformed_text}  → {transformed_pred}")
        print("MR Satisfied" if original_pred == transformed_pred else "MR Violated")
    finally:
        driver.quit()
