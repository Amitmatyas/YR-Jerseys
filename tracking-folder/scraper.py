import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_scraper():
    tracking_number = "כאן_שים_מספר_מעקב" # שים פה את המספר שלך
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(f"https://www.aftership.com/track/{tracking_number}")
        
        # מחכה לטעינת הסטטוס
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "status-tag")))
        
        status = driver.find_element(By.CLASS_NAME, "status-tag").text
        checkpoints = driver.find_elements(By.CLASS_NAME, "checkpoint-item")
        history = [cp.text.replace('\n', ' ') for cp in checkpoints]

        output = {
            "tracking_number": tracking_number,
            "status": status,
            "history": history,
            "last_update": time.strftime("%d/%m/%Y %H:%M")
        }

        # שמירה לקובץ JSON ספציפי שלא יפריע ל-index
        with open('tracking_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
        print("Success: tracking_data.json updated!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()
