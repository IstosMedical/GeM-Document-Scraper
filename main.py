# dependencies
import time
import os
from actions import enter_captcha
from actions import enter_captcha_and_download
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# initializing the Chrome webdriver instance
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)

# GeM All Bids URL (instead of contracts)
driver.get('https://bidplus.gem.gov.in/all-bids')

# enter captcha before loading bids
enter_captcha(driver=driver, captcha_code='captcha_code1', img_id='captchaimg1')

# keep scrolling to load all the bids
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element((By.ID, "load_more"))
        )
        print("All bids are loaded. Stopping scroll.")
        break
    except:
        print("Scrolling down... More bids loading.")

# number of bids available
documents = driver.find_elements(By.CLASS_NAME, "block_list")
print(f"Number of loaded bids: {len(documents)}")

# downloading the bid documents
for doc in documents:
    try:
        document_link = doc.find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].click();", document_link)
        time.sleep(2)
        enter_captcha_and_download(driver=driver, captcha_code="captcha_code")
    except Exception as e:
        print(f"Skipping one bid due to error: {e}")

print(f"🎉 Script finished! Total bids downloaded: {len(documents)}")

# waiting and quitting the webdriver instance
time.sleep(5)
driver.quit()
