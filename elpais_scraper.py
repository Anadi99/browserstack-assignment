import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from collections import Counter
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import time

# Step 1: Scrape El País Titles
url = "https://elpais.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
headlines = soup.find_all("h2")

article_data = []
for h in headlines[:10]:  # Top 10 for demo purposes
    title = h.get_text(strip=True)
    article_data.append({"title": title})

# Step 2: Translate Titles
translator = Translator()
english_titles = []

for article in article_data:
    translated = translator.translate(article["title"], src='es', dest='en')
    english_titles.append(translated.text)
    print("Title (Translated):", translated.text)

# Step 3: Analyze Words
words = []
for title in english_titles:
    words += re.findall(r'\b\w+\b', title.lower())

word_counts = Counter(words)
repeated = {word: count for word, count in word_counts.items() if count > 1}

print("\nRepeated Words:")
for word, count in repeated.items():
    print(f"{word}: {count}")

# Step 4: BrowserStack Automation
def run_browserstack_test(bstack_options, browser_name):
    username = "anadimishra_wxz4bz"
    access_key = "qzEvvLzpXd8psVH4Nmyq"
    remote_url = f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub"

    options = webdriver.ChromeOptions()
    options.set_capability("bstack:options", bstack_options)
    options.set_capability("browserName", browser_name)

    try:
        driver = webdriver.Remote(command_executor=remote_url, options=options)
        driver.get("https://elpais.com/")
        print(f"Page title on {bstack_options.get('sessionName')}: {driver.title}")
        time.sleep(5)
        driver.quit()
    except Exception as e:
        print(f"Error on {bstack_options.get('sessionName')}: {e}")

# Define capabilities
capabilities_list = [
    ({
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "Win-Chrome",
        "buildName": "ElPais Test"
    }, "Chrome"),
    ({
        "os": "OS X",
        "osVersion": "Monterey",
        "sessionName": "Mac-Firefox",
        "buildName": "ElPais Test"
    }, "Firefox"),
    ({
        "deviceName": "iPhone 13 Pro",
        "osVersion": "15",
        "realMobile": "true",
        "sessionName": "iPhone Test",
        "buildName": "ElPais Test"
    }, "iPhone"),
    ({
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "Edge-Win",
        "buildName": "ElPais Test"
    }, "Edge"),
    ({
        "deviceName": "Samsung Galaxy S22",
        "osVersion": "12.0",
        "realMobile": "true",
        "sessionName": "Android Test",
        "buildName": "ElPais Test"
    }, "Android")
]

# Run all tests in parallel
threads = []
for bstack_options, browser_name in capabilities_list:
    t = threading.Thread(target=run_browserstack_test, args=(bstack_options, browser_name))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
